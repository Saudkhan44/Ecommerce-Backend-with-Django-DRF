from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.cart.models import Cart
from .models import Order, OrderItem

class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user):
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.select_related("product").all()

        if not cart_items.exists():
            raise ValueError("Cart is empty")

        total_price = 0
        order = Order.objects.create(user=user, total_price=0)

        # --- DECREASE STOCK ---
        for item in cart_items:
            product = item.product
            if item.quantity > product.stock:
                print(item.quantity)
                raise ValueError(f"Not enough stock for {product.name}")

            product.stock -= item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=item.price
            )

            total_price += item.price * item.quantity

        order.total_price = total_price
        order.save()

        # --- CLEAR CART ---
        cart_items.delete()

        return order

    @staticmethod
    def cancel_order(user, order_id):
        order = get_object_or_404(Order, id=order_id, user=user)

        if order.status == "cancelled":
            order.status = "cancelled"
            order.save()
            return order

        if order.status != "pending":
            raise ValueError("Order cannot be cancelled")

        # --- RESTORE STOCK ---
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()

        order.status = "cancelled"
        order.save()

        return order


    @staticmethod
    def get_user_orders(user):
        """
        Get all orders for a user
        """
        return Order.objects.filter(user=user).order_by("-created_at")


    @staticmethod
    def get_order_detail(user, order_id):
        """
        Get specific order belonging to a user
        """
        return get_object_or_404(Order, id=order_id, user=user)

    @staticmethod
    @transaction.atomic
    def update_order_status(order_id, status_value):
        """
        Admin updates order status
        """

        order = get_object_or_404(Order, id=order_id)

        valid_status = [choice[0] for choice in Order.STATUS_CHOICES]

        if status_value not in valid_status:
            raise ValueError("Invalid order status")

        previous_status = order.status

        # Restore stock if admin cancels order
        if status_value == "cancelled" and previous_status != "cancelled":

            if previous_status in ["pending", "processing"]:
                for item in order.items.select_related("product").all():
                    if item.product:
                        item.product.stock += item.quantity
                        item.product.save(update_fields=["stock"])

        order.status = status_value
        order.save(update_fields=["status"])

        return order