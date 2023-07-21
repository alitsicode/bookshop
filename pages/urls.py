from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('detail/<int:pk>',views.ProductDetailView.as_view(),name='detail'),
    path('category_product/<int:pk>',views.ProductOfCategoryListView.as_view(),name='category_product'),
    path('search/',views.search_product.as_view(),name='search'),
    
]
