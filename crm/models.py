from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=255, default="Unknown")  # Default to avoid migration conflict
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Auto-calculate total_amount before saving
        total = sum(product.price for product in self.products.all())
        self.total_amount = total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"
models.CharField(max_length=100)
