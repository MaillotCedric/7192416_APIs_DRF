from rest_framework.serializers import ModelSerializer, SerializerMethodField

from shop.models import Category, Product, Article

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "category"]

class CategorySerializer(ModelSerializer):
    products = SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated", "products"]
    
    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)

        return serializer.data

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "date_created", "date_updated", "name", "price", "product"]
