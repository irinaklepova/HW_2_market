from django.shortcuts import render


def index(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({phone}, {email}):{message}')
    return render(request, 'catalog/contacts.html')
