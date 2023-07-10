from .models import Category,Product
def show_category(request):
    categories=Category.objects.all()
    return {'categories':categories}

def show_products(request):
    all_product=Product.objects.all()
    return {'all_product':all_product}
