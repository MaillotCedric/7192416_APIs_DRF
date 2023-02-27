from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product

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

    def get_products_details(self, products):
            return [
                {
                    "id": product.pk,
                    "date_created": self.format_datetime(product.date_created),
                    "date_updated": self.format_datetime(product.date_updated),
                    "name": product.name,
                    "category": product.category_id
                } for product in products
            ]
    
    def test_details(self):
        url_detail = reverse("category-detail",kwargs={"pk": self.category.pk})
        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, 200)

        expected = {
            "id": self.category.id,
            "name": self.category.name,
            "date_created": self.format_datetime(self.category.date_created),
            "date_updated": self.format_datetime(self.category.date_updated),
            "products": self.get_products_details(self.category.products.filter(active=True))
        }

        self.assertEqual(expected, response.json())
    
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

        self.assertEqual(response.json()["results"], expected)
    
    def test_create(self):
        category_count = Category.objects.count()

        response = self.client.post(self.url, data={"name": "Nouvelle catégorie"})

        self.assertEqual(response.status_code, 405)

        self.assertEqual(Category.objects.count(), category_count)

class TestProduct(ShopAPITestCase):
    url = reverse_lazy("product-list")

    def get_products_details(self, products):
        return [
            {
                "id": product.pk,
                "date_created": self.format_datetime(product.date_created),
                "date_updated": self.format_datetime(product.date_updated),
                "name": product.name,
                "category": product.category_id
            } for product in products
        ]
    
    def test_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_products_details([self.product, self.product_2]), response.json()["results"])
    
    def test_list_filter(self):
        response = self.client.get(self.url + "?category_id=%i" %self.category.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_products_details([self.product]), response.json()["results"])
    
    def test_create(self):
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={"name": "Nouvelle catégorie"})

        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)
    
    def test_delete(self):
        response = self.client.delete(reverse("product-detail", kwargs={"pk": self.product.pk}))

        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
