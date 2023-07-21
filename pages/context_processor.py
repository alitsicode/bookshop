from .models import Category,Product,AboutUs
def show_category(request):
    categories=Category.objects.all()
    return {'categories':categories}

def show_products(request):
    all_product=Product.objects.all()
    return {'products':all_product}

def show_info(request):
    info=AboutUs.objects.last()
    return {'info':info}
