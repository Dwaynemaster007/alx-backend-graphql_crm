from crm.models import Customer, Product
import random

def run():
    customers = [
        {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol", "email": "carol@example.com"},
    ]

    products = [
        {"name": "Laptop", "price": 999.99, "stock": 10},
        {"name": "Phone", "price": 499.99, "stock": 20},
        {"name": "Tablet", "price": 299.99, "stock": 15},
    ]

    for c in customers:
        Customer.objects.get_or_create(**c)

    for p in products:
        Product.objects.get_or_create(**p)

    print("Database seeded successfully!")

