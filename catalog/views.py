from django.urls import reverse_lazy, reverse
from catalog.models import Product
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Носки сделают ваш день!',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all()[:3]
        return context_data


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Информация о товарах',
    }


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Информация о товаре',
    }


class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'product_description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'product_description', 'image', 'category', 'price')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.object.pk])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'
