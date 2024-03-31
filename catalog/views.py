from django.shortcuts import render

from catalog.models import Product


def index(request):
    object_list = Product.objects.all()
    context = {
        'object_list': object_list,
        'title': 'Носки сделают ваш день!',
    }
    return render(request, 'catalog/home.html', context)


def product_info(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
        'title': 'Информация о товаре',
    }
    return render(request, 'catalog/product_info.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({phone}, {email}):{message}')
    return render(request, 'catalog/contacts.html')
