from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import OrderService
from .serializers import OrderSerializer


class CreateOrderView(APIView):
    """
    Checkout API
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            order = OrderService.create_order(request.user)
            serializer = OrderSerializer(order)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserOrdersView(APIView):
    """
    Get all orders of logged-in user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = OrderService.get_user_orders(request.user)

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrderDetailView(APIView):
    """
    Get single order
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        order = OrderService.get_order_detail(request.user, order_id)

        serializer = OrderSerializer(order)

        return Response(serializer.data)

class CancelOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):

        try:
            order = OrderService.cancel_order(request.user, order_id)

            serializer = OrderSerializer(order)

            return Response(serializer.data)

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


from rest_framework.permissions import IsAdminUser


class UpdateOrderStatusView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):

        status_value = request.data.get("status")

        order = OrderService.update_order_status(order_id, status_value)

        serializer = OrderSerializer(order)

        return Response(serializer.data)

    class UpdateOrderStatusView(APIView):
        """
        Admin can update order status
        """

        permission_classes = [IsAdminUser]

        def patch(self, request, order_id):

            status_value = request.data.get("status")

            if not status_value:
                return Response(
                    {"error": "Status is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                order = OrderService.update_order_status(order_id, status_value)

                serializer = OrderSerializer(order)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )