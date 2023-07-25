from django.contrib import admin

from shop_app.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'quantity', 'category', 'updated_at', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
