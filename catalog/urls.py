from django.urls import path

from catalog.views import index, contacts
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
]
