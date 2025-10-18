import re
import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Customer, Product, Order


# ===============================
# GraphQL Types
# ===============================

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


# ===============================
# Input Types
# ===============================

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(default_value=0)


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(default_value=timezone.now())


# ===============================
# Helper Functions
# ===============================

def validate_phone(phone):
    """Validate phone number format."""
    if phone and not re.match(r"^\+?\d{7,15}$|^\d{3}-\d{3}-\d{4}$", phone):
        raise ValidationError("Invalid phone number format.")


# ===============================
# Mutations
# ===============================

# --- CreateCustomer ---
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        errors = []
        try:
            if Customer.objects.filter(email=input.email).exists():
                raise ValidationError("Email already exists.")
            validate_phone(input.phone)

            customer = Customer(
                name=input.name,
                email=input.email,
                phone=input.phone or ""
            )
            customer.save()
            return CreateCustomer(customer=customer, message="Customer created successfully.")
        except ValidationError as e:
            errors.append(str(e))
            return CreateCustomer(errors=errors)


# --- BulkCreateCustomers ---
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        created_customers = []
        errors = []

        for data in input:
            try:
                if Customer.objects.filter(email=data.email).exists():
                    raise ValidationError(f"Email {data.email} already exists.")
                validate_phone(data.phone)
                customer = Customer(name=data.name, email=data.email, phone=data.phone or "")
                customer.save()
                created_customers.append(customer)
            except ValidationError as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)


# --- CreateProduct ---
class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        errors = []
        try:
            if input.price <= 0:
                raise ValidationError("Price must be positive.")
            if input.stock < 0:
                raise ValidationError("Stock cannot be negative.")

            product = Product(name=input.name, price=input.price, stock=input.stock)
            product.save()
            return CreateProduct(product=product)
        except ValidationError as e:
            errors.append(str(e))
            return CreateProduct(errors=errors)


# --- CreateOrder ---
class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        errors = []
        try:
            try:
                customer = Customer.objects.get(pk=input.customer_id)
            except Customer.DoesNotExist:
                raise ValidationError("Invalid customer ID.")

            if not input.product_ids:
                raise ValidationError("At least one product must be selected.")

            products = Product.objects.filter(pk__in=input.product_ids)
            if products.count() != len(input.product_ids):
                raise ValidationError("One or more product IDs are invalid.")

            total_amount = sum(p.price for p in products)

            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
                order_date=input.order_date or timezone.now()
            )
            order.products.set(products)
            order.save()

            return CreateOrder(order=order)
        except ValidationError as e:
            errors.append(str(e))
            return CreateOrder(errors=errors)


# ===============================
# Root Query & Mutation
# ===============================

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_orders(root, info):
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

