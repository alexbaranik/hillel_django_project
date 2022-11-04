from django.contrib import admin

from shop.mixins.admin_mixins import ImageMixins
from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(ImageMixins, admin.ModelAdmin):
    filter_horizontal = ('products',)
    list_display = ('name', 'price', 'currency', 'sku', 'created_at',)
    list_filter = ('price', 'category',)
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(ImageMixins, admin.ModelAdmin):
    list_display = ('name', 'created_at')
