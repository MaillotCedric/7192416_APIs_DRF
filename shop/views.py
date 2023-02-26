from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product

from shop.serializers import CategorySerializer, ProductSerializer

class CategoryAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

class ProductAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get("category_id")

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
