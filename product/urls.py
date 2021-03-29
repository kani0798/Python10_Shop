from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('<str:slug>/', product_list, name='list'),
    path('product/<int:product_id>/', product_detail,
                                      name='detail'),
    path('product/create/', create_product,
                            name='create-product'),
    path('product/update/<int:product_id>/', update_product,
                            name='update-product'),
    path('product/delete/<int:product_id>/', delete_product,
                            name='delete-product'),
]

