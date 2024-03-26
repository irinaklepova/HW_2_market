from django.core.management import BaseCommand
import json
from catalog.models import Category, Product

filename = 'fixtures/catalog_data.json'


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """Здесь мы получаем данные из фикстуры с категориями"""

        with open(filename, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return [item for item in data if item["model"] == "catalog.category"]

    @staticmethod
    def json_read_products():
        """Здесь мы получаем данные из фикстуры с продуктами"""
        with open(filename, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return [item for item in data if item["model"] == "catalog.product"]

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов

        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category["pk"],
                         category_name=category["fields"]["category_name"],
                         category_description=category["fields"]["category_description"])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product["pk"],
                        product_name=product["fields"]["product_name"],
                        product_description=product["fields"]["product_description"],
                        image=product["fields"]["image"],
                        # получаем категорию из базы данных для корректной связки объектов
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"],
                        created_at=product["fields"]["created_at"],
                        updated_at=product["fields"]["updated_at"],)
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
