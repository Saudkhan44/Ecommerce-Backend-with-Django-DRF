from django.contrib import admin
from .models import Order, OrderItem
from .services import OrderService


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")

    inlines = [OrderItemInline]

    readonly_fields = ("user", "total_price", "created_at")

    def save_model(self, request, obj, form, change):
        """
        Use service layer when status changes
        """

        if change:
            old_order = Order.objects.get(pk=obj.pk)

            if old_order.status != obj.status:
                OrderService.update_order_status(obj.id, obj.status)
                return

        super().save_model(request, obj, form, change)