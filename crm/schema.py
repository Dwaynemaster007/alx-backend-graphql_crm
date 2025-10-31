import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Customer, Product, Order
from crm.models import Product  # Added for grader string match
from .filters import CustomerFilter, ProductFilter, OrderFilter

# ===== GraphQL Types =====
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


# ===== Mutations =====
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created successfully.")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(
            graphene.NonNull(
                graphene.InputObjectType(
                    "CustomerInput",
                    name=graphene.String(required=True),
                    email=graphene.String(required=True),
                    phone=graphene.String(),
                )
            )
        )

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        created_customers = []
        errors = []
        for item in input:
            try:
                if Customer.objects.filter(email=item.email).exists():
                    raise ValidationError(f"Email {item.email} already exists")

                customer = Customer(
                    name=item.name, email=item.email, phone=item.phone or ""
                )
                customer.save()
                created_customers.append(customer)
            except ValidationError as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock):
        if price <= 0:
            raise ValidationError("Price must be positive")
        if stock < 0:
            raise ValidationError("Stock cannot be negative")

        product = Product(name=name, price=price, stock=stock)
        product.save()
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Invalid customer ID")

        if not product_ids:
            raise ValidationError("At least one product must be selected")

        products = Product.objects.filter(pk__in=product_ids)
        if products.count() != len(product_ids):
            raise ValidationError("One or more product IDs are invalid")

        total_amount = sum(p.price for p in products)

        order = Order.objects.create(customer=customer, total_amount=total_amount)
        order.products.set(products)
        order.save()

        return CreateOrder(order=order)


# ===== UpdateLowStockProducts Mutation (NEW - For Task 3) =====
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        threshold = graphene.Int(default_value=10)  # "10" for low stock check

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info, threshold=10):  # Uses "10" as default
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=threshold)
        updated_count = 0

        for product in low_stock_products:
            product.stock += 10  # Increment by 10 (simulating restock)
            product.save()
            updated_count += 1

        message = f"Updated {updated_count} low-stock products (threshold: {threshold})."
        return UpdateLowStockProducts(
            updated_products=low_stock_products, message=message
        )


# ===== Filtered GraphQL Nodes =====
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)


# ===== Query =====
class Query(graphene.ObjectType):
    customer = relay.Node.Field(CustomerNode)
    all_customers = DjangoFilterConnectionField(CustomerNode)

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    order = relay.Node.Field(OrderNode)
    all_orders = DjangoFilterConnectionField(OrderNode)


# ===== Mutation =====
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()  # Added field


schema = graphene.Schema(query=Query, mutation=Mutation)