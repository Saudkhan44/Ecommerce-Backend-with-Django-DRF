from rest_framework.views import APIView
from rest_framework.response import Response

class HomeAPIView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({
            "platform": "Ecommerce API",
            "version": "1.0",
            "description": "Backend for ecommerce platform",
            "auth": {
                "register": "/api/users/register/",
                "login": "/api/users/login/"
            }
        })