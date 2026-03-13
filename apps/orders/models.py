from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.products.models import Product


# ======================================
# ORDERS
# ======================================
class Order(models.Model):
    """
    User orders
    - status: tracks order state
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email if self.user else 'Unknown'}"

# ======================================
# ORDER ITEMS
# ======================================
class OrderItem(models.Model):
    """
    Items in an order
    - price is snapshot of product at checkout (copied from CartItem)
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"

