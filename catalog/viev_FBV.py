from django.shortcuts import render
from catalog.models import Product


def index(request):
    object_list = Product.objects.all()[:3]
    context = {
        'object_list': object_list,
        'title': 'Носки сделают ваш день!',
    }
    return render(request, 'catalog/blog_list.html', context)


def products_list(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Информация о товарах',
    }
    return render(request, 'catalog/product_list.html', context)


def product_card(request, pk):
    object = Product.objects.get(pk=pk)
    context = {
        'object': object,
        'title': 'Информация о товаре',
    }
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({phone}, {email}):{message}')
    return render(request, 'catalog/contacts.html')
