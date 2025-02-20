from django.db import models
from accounts.models import CustomUser  # Importing the user model

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    rating = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to user
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total cost of order

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at purchase time

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
