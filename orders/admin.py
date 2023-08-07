from django.contrib import admin
from orders.models import Order, OrderProduct, Payment, ShippingConfig

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingConfig)
admin.site.register(OrderProduct)
admin.site.register(Payment)
