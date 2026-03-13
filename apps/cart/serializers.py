# apps/cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'total']

    def get_total(self, obj):
        return obj.get_total()