from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CreateProductForm, UpdateProductForm
from .models import Category, Product


class SearchListView(ListView):
    model = Product
    template_name = 'product/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(name__icontains=q) |
                                   Q(description__icontains=q))
        return queryset

# def home_page(request):
#     categories = Category.objects.all()
#     return render(request, 'product/home.html', {
#                            'categories': categories})

class CategoryListView(ListView):
    model = Category
    template_name = 'product/home.html'
    context_object_name =  'categories'


# def product_list(request, slug):
#     products = Product.objects.filter(category__slug=slug)
#     return render(request, 'product/list.html', locals())

class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('slug')
        queryset = queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('slug')
        return context


# def product_detail(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     return render(request, 'product/detail.html', {'product': product})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


# def create_product(request):
#     if request.method == 'POST':
#         product_form = CreateProductForm(request.POST,
#                                          request.FILES)
#         if product_form.is_valid():
#             product = product_form.save()
#             # product = Product.objects.create(**product_form.cleaned_data)
#             return redirect(product.get_absolute_url())
#     else:
#         product_form = CreateProductForm()
#     return render(request, 'product/create_product.html',
#                       {'product_form': product_form})

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/create_product.html'
    form_class = CreateProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context

# def update_product(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     product_form = UpdateProductForm(request.POST or None,
#                                      request.FILES or None,
#                                      instance=product)
#     if product_form.is_valid():
#         product_form.save()
#         return redirect(product.get_absolute_url())
#     return render(request, 'product/update_product.html',
#                   {'product_form': product_form})

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/update_product.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


# def delete_product(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     if request.method == 'POST':
#         slug = product.category.slug
#         product.delete()
#         return redirect('list', slug)
#     return render(request, 'product/delete_product.html',
#                   {'product': product})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        from django.urls import reverse
        # print(self.kwargs)
        return reverse('home')




#  Shopping cart views

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url='/account/login/')
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')





