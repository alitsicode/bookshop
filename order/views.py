from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
import json
from .mixins import deletemixin
from django.http import Http404
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from melipayamak.melipayamak import Api
import requests
from django.core.mail import send_mail
# Create your views here.

from cart.cart import Cart
from accounts.models import Customeuser
from django.views import generic
from .models import Order,OrderItem,OrderInfo,DiscountCode

from django.urls import reverse_lazy

# list of user's open orders
class UserOrders(LoginRequiredMixin,generic.ListView):
	template_name='order/listorder.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["cart"] = Cart(self.request)
		context["orders"] = Order.objects.filter(user=self.request.user).filter(paid=True)
		return context
	
	def get_queryset(self):
		object_list = Order.objects.filter(user=self.request.user).filter(paid=False) 
		return object_list

# delete order
class DeleteOrder(deletemixin,LoginRequiredMixin,generic.DeleteView):
	model=Order
	template_name='order/deleteorder.html'
	context_object_name='userorder'
	success_url=reverse_lazy('userorders')
	def form_valid(self, form):
		messages.error(self.request,_("your Order successfuly deleted"),'danger')
		return super().form_valid(form)

# detail of each user's orders
class OrderDetailView(LoginRequiredMixin, View):

	def get(self, request, order_id):
		order = get_object_or_404(Order, id=order_id)
		if request.user == order.user:
			return render(request, 'order/order.html', {'order':order})
		else:
			return Http404(_('you cant see people order'))

# create order
@login_required
def OrderCreateView(request):
	cart = Cart(request)
	if request.method=='POST':
		order = Order.objects.create(user=request.user,info=request.user.orderinfo.last())
		for item in cart:
			if item['product_obj'].is_discount:
				orderitem=OrderItem.objects.create(order=order, product=item['product_obj'], price=item['product_obj'].price_with_discount, quantity=item['quantity'])
				order.order_total_price +=orderitem.price*orderitem.quantity+350000
			else:
				orderitem=OrderItem.objects.create(order=order, product=item['product_obj'], price=item['product_obj'].price, quantity=item['quantity'])
				order.order_total_price +=orderitem.price*orderitem.quantity+350000
			order.save()
		cart.clear()
		messages.success(request,_("your order successfuly created"),'success')
		
		return redirect('order_detail', order.id)
	info = OrderInfo.objects.filter(user=request.user).last()
	return render(request,'order/order_create.html', {'infos': info,})
	

# user information to recieve product
class OrderInfoCreate(LoginRequiredMixin,generic.CreateView):
	model=OrderInfo
	template_name='order/info.html'
	success_url=reverse_lazy('order_create')
	fields=['name','last_name','address','phone_number']

	def form_valid(self,form):
		instance=form.save(commit=False)
		instance.user=self.request.user
		instance.save()
		messages.success(self.request,_("your recieve info successfuly add"),'success')
		return super().form_valid(form)

class ApplyDiscountView(View):
	def post(self,request,pk):
		code=request.POST.get('discount_code')
		order=get_object_or_404(Order,pk=pk)
		discount_code=get_object_or_404(DiscountCode,name=code)
		for used in discount_code.user_used.all():
			if discount_code.quantity==0 or request.user==used :
				messages.error(self.request,_("discount code expired or you used it one time before"),'danger')
				return redirect('order_detail',order.id)
		if discount_code.discount_price_send :
			order.order_total_price -=350000
		if 5000000 <= order.order_total_price <=9999999:
			order.order_total_price -=discount_code.discount_price1
		elif 10000000 <= order.order_total_price <=19999999:
			order.order_total_price -=discount_code.discount_price2
		elif 20000000 <= order.order_total_price :
			order.order_total_price -=discount_code.discount_price3
		
		order.save()
		discount_code.user_used.add(request.user)
		discount_code.quantity -=1
		discount_code.save()
		messages.success(self.request,_("your discount code successfully apply"),'success')
		return redirect('order_detail',order.id)

# sand box mode
# MERCHANT = 'ABFGbdhttyifkddfhrBFShggklerigoFJnfI'
# ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
# ///////////////////////////////////////////////////////////////////////
MERCHANT = '37779b5f-695a-418d-a6d2-83613b5f100f'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
description = "توضیحات مربوط به تراکنش "
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"



# # gateway to pay
class OrderPayView(LoginRequiredMixin,View):
	def get(self, request, order_id):
		order = Order.objects.get(id=order_id)
		req_data = {
			"merchant_id": MERCHANT,
			"amount": order.order_total_price ,
			"callback_url": f'http://127.0.0.1:8000/order/verify/{order.id}',
			"description": description,
		}
		req_header = {"accept": "application/json","content-type": "application/json'"}
		req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
			req_data), headers=req_header)
		authority = req.json()['data']['authority']
		if len(req.json()['errors']) == 0:
			return redirect(ZP_API_STARTPAY.format(authority=authority))
		else:
			e_code = req.json()['errors']['code']
			e_message = req.json()['errors']['message']
			return HttpResponse(f"کد خطا: {e_code}, متن خطا: {e_message}")

# # after pay successfuly
class OrderVerifyView(LoginRequiredMixin,View):
	def get(self, request,order_id):
		order = Order.objects.get(id=order_id)
		t_status = request.GET.get('Status')
		t_authority = request.GET['Authority']
		if request.GET.get('Status') == 'OK':
			req_header = {"accept": "application/json",
						  "content-type": "application/json'"}
			req_data = {
				"merchant_id": MERCHANT,
				"amount": order.order_total_price,
				"authority": t_authority
			}
			req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
			if len(req.json()['errors']) == 0:
				t_status = req.json()['data']['code']
				if t_status == 100:
					order.paid = True
					order.save()
					content = {
					'type' : 'تراکنش موفق',
                    'ref_id' : str(
					 	req.json()['data']['ref_id']
                    )}
					msg=f' : سلام امیدواریم از خریدتان راضی باشید. اطلاعات خرید شما \n {request.user.username} : کاربر \n  هزینه ی ارسال:35,000 تومان \n  {order.order_total_price//10} : قیمت نهایی تومان \n {order.info.address} : آدرس\n' 
					send_mail("ثبت سفارش ",msg,'ak2727027@gmail.com',[request.user.email])
					
					username = '09226652413'
					password = '7185bh'
					api = Api(username,password)
					sms = api.sms()
					to = str(request.user.phone)
					_from = '50004001652413'
					text = msg
					response = sms.send(to,_from,text)
					print(response)
					return render(request, 'order/transaction_status.html', context=content)
					# return HttpResponse('تراکنش موفق.\nRefID: ' + str(
					# 	req.json()['data']['ref_id']
					# ))
				elif t_status == 101:
					content = {
					'type' : 'تراکنش قبلا انجام شده',
                    'message' : str(
					 	req.json()['data']['message']
                    )}
					return render(request, 'order/transaction_status.html', context=content)
					# return HttpResponse('تراکنش قبلا انجام شده : ' + str(
					# 	req.json()['data']['message']
					# ))
				else:
					content = {
					'type' : 'تراکنش ناموفق',
                    'message' : str(
					 	req.json()['data']['message']
                    )}
					return render(request, 'order/transaction_status.html', context=content)
					# return HttpResponse('تراکنش ناموفق.\nStatus: ' + str(
					# 	req.json()['data']['message']
					# ))
			else:
				e_code = req.json()['errors']['code']
				e_message = req.json()['errors']['message']
				content = {
					'type' : f'کد خطا : {e_code}',
                    'message' : f'متن خطا : {e_message}'
				}
				return render(request, 'order/transaction_status.html', context=content)
				# return HttpResponse(f"کد خطا: {e_code}, متن خطا: {e_message}")
		else:
				content = {
                    'type' : 'تراکنش ناموفق بود یا توسط کاربر لغو شد'
				}
				return render(request, 'order/transaction_status.html', context=content)
			# return HttpResponse('تراکنش ناموفق بود یا توسط کاربر لغو شد')


# class OrderPayViewsandbox(LoginRequiredMixin, View):
# 	def get(self, request, order_id):
# 		order = Order.objects.get(id=order_id)
# 		CallbackURL = f'http://127.0.0.1:8000/order/verify_sandbox/{order.id}'
# 		req_data = {
# 			"MerchantID": MERCHANT,
# 			"Amount": order.order_total_price,
# 			"CallbackURL": CallbackURL,
# 			"Description": description,
# 		}
# 		req_header = {"accept": "application/json","content-type": "application/json'"}
# 		req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
# 			req_data), headers=req_header)
# 		print(req.json())
# 		authority=req.json()['Authority']
# 		if 'errors' or len(req.json()['errors']) == 0:
# 			return redirect(ZP_API_STARTPAY.format(authority=authority),order.id)
# 		else:
# 			return HttpResponse('you got error')

# class OrderVerifyViewsandbox(LoginRequiredMixin, View):
# 	def get(self, request,order_id):
# 		order = Order.objects.get(id=order_id)
# 		t_status = request.GET.get('Status')
# 		t_authority = request.GET['Authority']
# 		if request.GET.get('Status') == 'OK':
# 			req_header = {"accept": "application/json",
# 						  "content-type": "application/json'"}
# 			req_data = {
# 				"MerchantID": MERCHANT,
# 				"Amount": order.order_total_price,
# 				"Authority": t_authority
# 			}
# 			req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
# 			if 'errors' or len(req.json()['errors']) == 0:
# 				t_status = req.json()['Status']
# 				print(t_status)
# 				if t_status == 100:
# 					order.paid = True
# 					order.save()
# 					content = {
# 					'type' : 'تراکنش موفق',
# 					'ref_id' : str(
# 					req.json()
#                     )}
# 					return render(request, 'order/transaction_status.html', context=content)
# 				elif t_status == 101:
# 					content = {
# 						'type' : 'تراکنش قبلا انجام شده',
# 						'message' : str(req.json())
# 					}
# 					return render(request, 'order/transaction_status.html', context=content)
# 				else:
# 					content = {
# 						'type' : 'تراکنش ناموفق',
# 						'message' : str(req.json())
# 					}
# 					return render(request, 'order/transaction_status.html', context=content)
# 			else:
# 				content = {
# 					'type' :'اووووه نه'
# 				}
# 				return render(request, 'order/transaction_status.html', context=content)
# 		else:
# 			content = {
# 				'type' : 'تراکنش ناموفق بود یا توسط کاربر لغو شد'
# 			}
# 			return render(request, 'order/transaction_status.html', context=content)