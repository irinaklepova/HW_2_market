from django.urls import path

from catalog.views import index, contacts, products_list, product_card
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', products_list, name='products_list'),
    path('products/<int:pk>/', product_card, name='product_card'),
]
