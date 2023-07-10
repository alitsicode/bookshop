from django.shortcuts import render,get_object_or_404
from .models import Category,Product
from django.views import generic

# Create your views here.

def home(request):
    products=Product.objects.all()
    return render(request,'pages/home.html',context={'products':products})

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "pages/detail.html"
    context_object_name='product'

class ProductOfCategoryListView(generic.ListView):
    template_name='pages/home.html'
    model=Category
    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        categorie=get_object_or_404(Category,pk=pk)
        product_category=categorie.product.all()
        context = super().get_context_data(**kwargs)
        context["products"] = product_category
        return context