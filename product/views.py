from django.shortcuts import render

from .models import Category, Product


def home_page(request):
    categories = Category.objects.all()
    return render(request, 'product/home.html', {
                           'categories': categories})


def product_list(request, slug):
    products = Product.objects.filter(category__slug=slug)
    return render(request, 'product/list.html', locals())


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product/detail.html', {'product': product})






