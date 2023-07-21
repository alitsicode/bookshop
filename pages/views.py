from django.shortcuts import render,get_object_or_404
from .models import Category,Product
from django.views import generic
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request,'pages/home.html')

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

class search_product(generic.ListView):
    template_name='pages/home.html'
    model=Product
    context_object_name='products'
    # paginate_by=9
    def get_queryset(self):
        query=self.request.GET.get("search")
        products = Product.objects.all().filter(Q(title__icontains=query)) 
        return products