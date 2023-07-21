from django.contrib import admin
from .models import Order, OrderItem,OrderInfo,DiscountCode
from jalali_date import datetime2jalali, date2jalali
# Register your models here.
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'get_created_jalali','info', 'paid','tracking_code')
	ordering=('-paid',)
	list_filter = ('paid',)
	inlines = (OrderItemInline,)
	def get_created_jalali(self, obj):
		return datetime2jalali(obj.created).strftime('%A, %d %b %Y %H:%M:%S')
	get_created_jalali.short_description = "ثبت سفارش"

@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
	list_display = ('user','name','last_name','address','phone_number')

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
	list_display = ('name','discount_price1','discount_price2','discount_price3','discount_price_send','quantity')
	ordering=['-created']
	search_fields=['name']