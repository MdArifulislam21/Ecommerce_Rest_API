from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, ProductViewSet

app_name = "products"

# initialize DefaultRouter class
router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"", ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
