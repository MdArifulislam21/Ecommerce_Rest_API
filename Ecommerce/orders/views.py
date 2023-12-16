from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from orders.models import Order, OrderItem
from orders.permissions import (
    IsOrderByBuyer,
    IsOrderItemByBuyer,
    IsOrderItemPending,
    IsOrderPending,
)
from orders.serializers import (
    OrderItemSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD order items that are associated with the current order id.
    """

    queryset = OrderItem.objects.all().select_related("product", "order")
    serializer_class = OrderItemSerializer
    permission_classes = [IsOrderItemByBuyer]

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get("order_id")
        return res.filter(order__id=order_id)

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        serializer.save(order=order)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes += [IsOrderItemPending]

        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD orders of a user
    """

    queryset = Order.objects.all().select_related("buyer","shipping_address","billing_address").prefetch_related("order_items")
    permission_classes = [IsOrderByBuyer]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(buyer=user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()
