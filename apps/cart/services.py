from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from django.utils import timezone


class CartService:
    """All cart business logic for user carts"""

    @staticmethod
    def get_or_create_cart(user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def add_item(user, product_id, quantity=1):
        """
        Add product to cart

        Rules:
        - If new item → add with given quantity
        - If existing item → increase only by +1
        """

        cart = CartService.get_or_create_cart(user)
        product = get_object_or_404(Product, id=product_id)

        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product
        ).first()

        # -------------------------
        # EXISTING ITEM IN CART
        # -------------------------
        if cart_item:

            if cart_item.quantity + 1 > product.stock:
                raise ValidationError("Cannot add more than available stock")

            cart_item.quantity += 1
            cart_item.save()

        # -------------------------
        # NEW ITEM IN CART
        # -------------------------
        else:

            if quantity > product.stock:
                raise ValidationError("Cannot add more than available stock")

            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price=product.price
            )

        cart.updated_at = timezone.now()
        cart.save()

        return cart_item


    @staticmethod
    def update_quantity(user, product_id, quantity):
        """
        Update cart item quantity manually
        """

        cart = CartService.get_or_create_cart(user)

        cart_item = get_object_or_404(
            CartItem,
            cart=cart,
            product_id=product_id
        )

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0")

        if quantity > cart_item.product.stock:
            raise ValidationError("Cannot set quantity more than available stock")

        cart_item.quantity = quantity
        cart_item.save()

        cart.updated_at = timezone.now()
        cart.save()

        return cart_item


    @staticmethod
    def remove_item(user, product_id):
        cart = CartService.get_or_create_cart(user)

        cart_item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).first()

        if cart_item:
            cart_item.delete()

            cart.updated_at = timezone.now()
            cart.save()

            return True

        return False


    @staticmethod
    def get_cart_details(user):
        cart = CartService.get_or_create_cart(user)

        return {
            "cart": cart,
            "items": cart.items.select_related("product"),
            "total": cart.get_total()
        }