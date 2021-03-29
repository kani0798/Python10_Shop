from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateProductForm, UpdateProductForm
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


def create_product(request):
    if request.method == 'POST':
        product_form = CreateProductForm(request.POST,
                                         request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            # product = Product.objects.create(**product_form.cleaned_data)
            return redirect(product.get_absolute_url())
    else:
        product_form = CreateProductForm()
    return render(request, 'product/create_product.html',
                      {'product_form': product_form})


def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_form = UpdateProductForm(request.POST or None,
                                     request.FILES or None,
                                     instance=product)
    if product_form.is_valid():
        product_form.save()
        return redirect(product.get_absolute_url())
    return render(request, 'product/update_product.html',
                  {'product_form': product_form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        slug = product.category.slug
        product.delete()
        return redirect('list', slug)
    return render(request, 'product/delete_product.html',
                  {'product': product})





