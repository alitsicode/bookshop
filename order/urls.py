from django.urls import path
from . import views

urlpatterns = [
	path('create/', views.OrderCreateView, name='order_create'),
	path('infocreate/', views.OrderInfoCreate.as_view(), name='order_infocreate'),
	path('delete/<int:pk>', views.DeleteOrder.as_view(), name='order_delete'),
	path('show/', views.UserOrders.as_view(), name='userorders'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
	path('discount/<int:pk>', views.ApplyDiscountView.as_view(), name='discount'),
    # ////////////////////////////////////////////////////////////////////////////////////
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    # path('pay_sandbox/<int:order_id>/', views.OrderPayViewsandbox.as_view(), name='order_pay'),
    # path('verify_sandbox/<int:order_id>/', views.OrderVerifyViewsandbox.as_view(), name='order_verify'),

]