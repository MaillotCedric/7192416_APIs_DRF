from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "date_created", "date_updated", "name", "price", "product"]

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "category"]

class ProductDetailsSerializer(ModelSerializer):
    articles = SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "date_created", "date_updated", "name", "category", "articles"]
    
    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)

        return serializer.data

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated"]
    
    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError("La catégorie existe déjà")
        
        return value

class CategoryDetailsSerializer(ModelSerializer):
    products = SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated", "products"]
    
    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)

        return serializer.data
