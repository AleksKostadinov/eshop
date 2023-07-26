from django.contrib import admin

from shop_app.models import Category, Gender, Product

class GenderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('gender_name',)}
    list_display = ('gender_name', 'description')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'description')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'discount_percentage', 'discounted_price', 'quantity', 'category', 'updated_at', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Product, ProductAdmin)
