from django.contrib import admin
from .models import Brand, Product


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'amazon_url')
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'asin', 'sku', 'image', 'brand')
    search_fields = ['brand__name', 'name', 'asin']
