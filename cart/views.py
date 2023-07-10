from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from .forms import add_to_cart_form
from django.utils.translation import gettext_lazy as _
from pages.models import Product
from django.contrib import messages
from django.views.decorators.http import require_POST
# Create your views here.
def cart_view(request):
    cart=Cart(request)
    for item in cart:
        item['product_update_number_form']=add_to_cart_form(initial={'quantity':item['quantity'],'inplace':True})
    return render(request,'cart/cart.html',context={'cart':cart})

@require_POST
def add_to_cart(request,product_id):
    cart=Cart(request)
    pro=get_object_or_404(Product,id=product_id)
    form=add_to_cart_form(request.POST)
    if form.is_valid():
        cleaned_data=form.cleaned_data
        quantity=cleaned_data['quantity']
        cart.add(pro,quantity,replace_quantity=cleaned_data['inplace'])
        messages.success(request,_('successfuly added to cart'),'success')
    return redirect('home') #if you want to redirect after each add to cart
def remove_from_cart(request,product_id):
    cart=Cart(request)
    pro=get_object_or_404(Product,id=product_id)
    cart.remove(pro)
    messages.error(request,_('successfuly removed from cart'),'danger')
    return redirect('/cart') #if you want to redirect after each add to cart


# Create your views here.
