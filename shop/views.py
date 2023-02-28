from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action

from shop.models import Category, Product, Article

from shop.serializers import CategoryDetailsSerializer, CategoryListSerializer, ProductDetailsSerializer, ProductListSerializer, ArticleSerializer

class MultipleSerializerMixin:
    details_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.details_serializer_class is not None:
            return self.details_serializer_class
        
        return super().get_serializer_class()

class CategoryAPIViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    details_serializer_class = CategoryDetailsSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    @action(detail=True, methods=["post"])
    def disable(self, request, pk):
        self.get_object().disable()

        return Response()

class ProductAPIViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    details_serializer_class = ProductDetailsSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get("category_id")

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    @action(detail=True, methods=["post"])
    def disable(self, request, pk):
        self.get_object().disable()

        return Response()

class ArticleAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get("product_id")

        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)

        return queryset

class AdminCategoryAPIViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    details_serializer_class = CategoryDetailsSerializer

    def get_queryset(self):
        return Category.objects.all()
