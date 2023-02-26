from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from shop.views import CategoryAPIViewSet, ProductAPIViewSet

router = routers.SimpleRouter()

router.register("category", CategoryAPIViewSet, basename="category")
router.register("product", ProductAPIViewSet, basename="product")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
