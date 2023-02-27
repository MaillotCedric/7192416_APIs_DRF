from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category

class ShopAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Fruits", active=True)

        Category.objects.create(name="Légumes", active=False)

        cls.product = cls.category.products.create(name="Ananas", active=True)

        cls.category.products.create(name="Banane", active=False)

        cls.category_2 = Category.objects.create(name="Épicerie", active=True)
        cls.product_2 = cls.category_2.products.create(name="Sel", active=True)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

class TestCategory(ShopAPITestCase):
    url = reverse_lazy("category-list") # <basename>-list
    
    def test_list(self): # test si les catégories retournées sont seulement celles qui sont actives
        response = self.client.get(self.url)

        # vérification du status_code
        self.assertEqual(response.status_code, 200)

        # Vérification des données
        expected = [
            {
                "id": category.id,
                "name": category.name,
                "date_created": self.format_datetime(category.date_created),
                "date_updated": self.format_datetime(category.date_updated)
            } for category in [self.category, self.category_2]
        ]

        self.assertEqual(response.json(), expected)
    
    def test_create(self):
        category_count = Category.objects.count()

        response = self.client.post(self.url, data={"name": "Nouvelle catégorie"})

        self.assertEqual(response.status_code, 405)

        self.assertEqual(Category.objects.count(), category_count)
