from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductCreateAPIView,
    ProductUpdateDeleteAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDeleteAPIView,
    ProductImageUploadAPIView
)

urlpatterns = [

    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryRetrieveUpdateDeleteAPIView.as_view(), name="category-detail"),

    path("", ProductListAPIView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),

    path("create/", ProductCreateAPIView.as_view(), name="product-create"),
    path("manage/<int:pk>/", ProductUpdateDeleteAPIView.as_view(), name="product-manage"),

    path("upload-image/", ProductImageUploadAPIView.as_view(), name="product-image-upload"),
]