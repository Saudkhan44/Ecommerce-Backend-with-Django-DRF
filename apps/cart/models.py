# apps/cart/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.products.models import Product


class Cart(models.Model):
    """One cart per user"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart of {self.user.email}"

    def get_total(self):
        """Calculate total price of all items in the cart"""
        return sum(item.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Items in cart with snapshot of price"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"