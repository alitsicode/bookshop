from django.contrib import admin
from .models import Category,Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','cover_tag']
    search_fields=['title']
    ordering=['-created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','price','is_discount','price_with_discount','image_tag']
    list_filter=['category']
    ordering=['-created']
    search_fields=['title']

