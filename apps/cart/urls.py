# apps/cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartView.as_view(), name="cart-detail"),
    path("add/", views.CartAddItemView.as_view(), name="cart-add"),
    path("update/<int:product_id>/", views.CartUpdateItemView.as_view(), name="cart-update"),
    path("remove/<int:product_id>/", views.CartRemoveItemView.as_view(), name="cart-remove"),
]