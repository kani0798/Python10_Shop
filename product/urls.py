from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('<str:slug>/', product_list, name='list'),
    path('product/<int:product_id>/', product_detail,
                                      name='detail'),
]

