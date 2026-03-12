from django.contrib import admin
from .models import CustomUser
from apps.products.models import Category, Product, ProductImage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(CustomUser)