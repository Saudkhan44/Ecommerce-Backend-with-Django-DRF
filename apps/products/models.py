from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings



# ======================================
# CATEGORIES
# ======================================
class Category(models.Model):
    """
    Product categories
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# ======================================
# PRODUCTS
# ======================================
class Product(models.Model):
    """
    Product catalog
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['name']),
        ]

# ======================================
# PRODUCT IMAGES
# ======================================
class ProductImage(models.Model):
    """
    Multiple images per product.
    - image stored in /media/products/
    - is_primary: determines main display image
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Make all other images for this product non-primary
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"
