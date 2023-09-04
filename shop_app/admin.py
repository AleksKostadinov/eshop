import admin_thumbnails
from django.contrib import admin

from shop_app.models import (Brand, Category, Collection, Cover, Gender,
                             Product, ProductGallery, ReviewRating, Variation)


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class GenderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('gender_name',)}
    list_display = ('gender_name', 'description')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'description')


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}
    list_display = ('brand_name', 'description')


class CoverAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('cover_name',)}
    list_display = ('cover_name', 'cover_title')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'discounted_price', 'discount_percentage', 'collection', 'additional_discount_percentage', 'price', 'quantity', 'category',  'created_at', 'updated_at', 'is_available')
    list_filter = ('category', 'collection', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    readonly_fields = ('discounted_price_db', 'additional_discount_percentage')
    inlines = [ProductGalleryInline]


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('collection_name', 'start_date', 'end_date', 'additional_discount_percentage',)
    prepopulated_fields = {'slug': ('collection_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active', )
    list_filter = ('product', 'variation_category', 'variation_value', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Cover, CoverAdmin)
