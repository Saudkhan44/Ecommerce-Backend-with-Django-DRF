# apps/cart/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import CartService
from .serializers import CartSerializer, CartItemSerializer
from rest_framework import status


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_data = CartService.get_cart_details(request.user)
        serializer = CartSerializer(cart_data["cart"])
        return Response(serializer.data)


class CartAddItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        cart_item = CartService.add_item(request.user, product_id, quantity)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)


class CartUpdateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, product_id):
        quantity = int(request.data.get("quantity", 1))
        cart_item = CartService.update_quantity(request.user, product_id, quantity)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

class CartRemoveItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        success = CartService.remove_item(request.user, product_id)
        return Response({"deleted": success})