from django.test import TestCase

from alx_backend_graphql_crm.schema import schema

from .models import Customer, Order, Product


class CrmSchemaTests(TestCase):
    def run_query(self, query, **variables):
        result = schema.execute(query, variable_values=variables)
        return result

    def test_create_customer_and_duplicate_email(self):
        query = 'mutation($n:String!,$e:String!){ createCustomer(name:$n, email:$e){ customer{ name email } message } }'
        result = self.run_query(query, n='Alice', e='alice@example.com')
        self.assertIsNone(result.errors)
        self.assertEqual(result.data['createCustomer']['customer']['email'], 'alice@example.com')
        duplicate = self.run_query(query, n='Alice 2', e='alice@example.com')
        self.assertIn('already exists', str(duplicate.errors[0]))

    def test_bulk_create_reports_errors_but_keeps_valid_rows(self):
        Customer.objects.create(name='Bob', email='bob@example.com')
        result = self.run_query('''mutation { bulkCreateCustomers(input: [
            {name: "Carol", email: "carol@example.com"},
            {name: "Bob again", email: "bob@example.com"}
        ]) { customers { email } errors } }''')
        self.assertIsNone(result.errors)
        data = result.data['bulkCreateCustomers']
        self.assertEqual([c['email'] for c in data['customers']], ['carol@example.com'])
        self.assertEqual(len(data['errors']), 1)

    def test_create_product_validates_price(self):
        ok = self.run_query('mutation { createProduct(name: "Laptop", price: 999.99, stock: 5) { product { name stock } } }')
        self.assertIsNone(ok.errors)
        bad = self.run_query('mutation { createProduct(name: "Free", price: 0) { product { name } } }')
        self.assertIn('positive', str(bad.errors[0]))

    def test_create_order_totals_products(self):
        customer = Customer.objects.create(name='Dan', email='dan@example.com')
        p1 = Product.objects.create(name='Mouse', price='20.00', stock=3)
        p2 = Product.objects.create(name='Pad', price='5.50', stock=3)
        result = self.run_query(
            'mutation($c:ID!,$p:[ID]!){ createOrder(customerId:$c, productIds:$p){ order{ totalAmount } } }',
            c=str(customer.pk), p=[str(p1.pk), str(p2.pk)],
        )
        self.assertIsNone(result.errors)
        self.assertEqual(float(result.data['createOrder']['order']['totalAmount']), 25.5)
        self.assertEqual(Order.objects.get().products.count(), 2)
        bad = self.run_query('mutation($c:ID!,$p:[ID]!){ createOrder(customerId:$c, productIds:$p){ order{ id } } }', c=str(customer.pk), p=['999'])
        self.assertIn('invalid', str(bad.errors[0]).lower())

    def test_filters_and_low_stock_restock(self):
        Product.objects.create(name='Cable', price='3.00', stock=2)
        Product.objects.create(name='Monitor', price='150.00', stock=40)
        result = self.run_query('{ allProducts(lowStock: true) { edges { node { name } } } }')
        self.assertIsNone(result.errors)
        self.assertEqual([e['node']['name'] for e in result.data['allProducts']['edges']], ['Cable'])
        restock = self.run_query('mutation { updateLowStockProducts { updatedProducts { name stock } message } }')
        self.assertIsNone(restock.errors)
        self.assertEqual(restock.data['updateLowStockProducts']['updatedProducts'][0]['stock'], 12)

    def test_customer_name_filter(self):
        Customer.objects.create(name='Eve Adams', email='eve@example.com')
        Customer.objects.create(name='Frank', email='frank@example.com')
        result = self.run_query('{ allCustomers(nameIcontains: "eve") { edges { node { email } } } }')
        self.assertEqual([e['node']['email'] for e in result.data['allCustomers']['edges']], ['eve@example.com'])
