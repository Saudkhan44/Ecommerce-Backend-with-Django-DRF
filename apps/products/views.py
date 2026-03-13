from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from .permissions import IsManagerOrReadOnly
from .filters import ProductFilter

class CategoryListCreateAPIView(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

class CategoryRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

class ProductListAPIView(generics.ListAPIView):

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

class ProductDetailAPIView(generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductCreateAPIView(generics.CreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

class ProductUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

class ProductImageUploadAPIView(generics.CreateAPIView):

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]