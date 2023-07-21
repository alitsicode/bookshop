from django.contrib import admin
from .models import Category,Product,AboutUs,Colors,Size
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

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display=['site_name','whatsapp_number','telegram_id','instagram_id','phone_number']
    ordering=['-created']

@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display=['color']
    search_fields=['color']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display=['size']
    search_fields=['size']
