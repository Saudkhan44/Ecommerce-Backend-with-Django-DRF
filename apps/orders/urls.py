from django.urls import path
from . import views

urlpatterns = [

    path("", views.UserOrdersView.as_view(), name="user-orders"),
    path("create/", views.CreateOrderView.as_view(), name="create-order"),
    path("<int:order_id>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("<int:order_id>/cancel/", views.CancelOrderView.as_view(), name="cancel-order"),
    path("admin/<int:order_id>/status/", views.UpdateOrderStatusView.as_view()),

]