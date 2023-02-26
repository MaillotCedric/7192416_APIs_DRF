from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from shop.views import CategoryAPIViewSet, ProductAPIView

router = routers.SimpleRouter()

router.register("category", CategoryAPIViewSet, basename="category")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/product/', ProductAPIView.as_view())
]
