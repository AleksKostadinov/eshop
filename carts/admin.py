from django.contrib import admin
from carts.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'purchased', 'created']

admin.site.register(Cart, CartAdmin)
