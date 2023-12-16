from rest_framework import permissions, viewsets

from products.models import Product, Category
from products.permissions import IsSeller
from products.serializers import (
    CategorySerializer,
    ProductReadOnlySerializer,
    ProductWriteSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    All category will retrieve in a list.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().select_related("category")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ProductWriteSerializer
        return ProductReadOnlySerializer

    def get_permissions(self):

        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        
            
        elif self.action in ("update", "partial_update", "destroy"):
            
            """
                Only the seller of that product can update of delete.
            """
            
            self.permission_classes = (IsSeller,)
            
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
