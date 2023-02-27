from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article

from shop.serializers import CategoryDetailsSerializer, CategoryListSerializer, ProductDetailsSerializer, ProductListSerializer, ArticleSerializer

class CategoryAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    details_serializer_class = CategoryDetailsSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.details_serializer_class
        
        return super().get_serializer_class()

class ProductAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    details_serializer_class = ProductDetailsSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get("category_id")

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.details_serializer_class

        return super().get_serializer_class()

class ArticleAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get("product_id")

        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)

        return queryset
