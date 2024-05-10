from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        products = Product.objects.all()
        for product in products:
            version = Version.objects.filter(product=product)
            current_version = version.filter(is_current=True).first()
            product.current_version = current_version.name if current_version else 'Версия неактивна'
        context_data['object_list'] = products
        return context_data


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Информация о товаре',
    }


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.creator_product = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data
    
    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'
