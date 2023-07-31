from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchased', 'created', 'user']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'sub_total', 'cart']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
