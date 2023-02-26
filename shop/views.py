from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product

from shop.serializers import CategorySerializer, ProductSerializer

class CategoryAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

class ProductAPIView(APIView):
    def get(self, *args, **kwargs):
        produits = Product.objects.all()
        serializer = ProductSerializer(produits, many=True)

        return Response(serializer.data)
