from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=200, verbose_name='Категория')
    category_description = models.TextField(max_length=500, verbose_name='Описание категории')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Наименование')
    product_description = models.TextField(max_length=500, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, **NULLABLE,
                                 verbose_name='Категория')
    price = models.IntegerField(verbose_name='Стоимость')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.product_name} {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('product_name',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.PositiveIntegerField(verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии', **NULLABLE)
    is_current = models.BooleanField(default=True, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.product} {self.number} {self.name}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
