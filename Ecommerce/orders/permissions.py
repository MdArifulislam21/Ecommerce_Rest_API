from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from rest_framework import permissions

from orders.models import Order


class IsOrderPending(BasePermission):
    """
    Check the status of order is pending or completed before updating/deleting instance
    """

    message = _("Updating or deleting closed order is not allowed.")

    def has_object_permission(self, request, view, obj):
        # if view.action in ("retrieve",):
        #     return True
        if request.method in permissions.SAFE_METHODS:
            # Permission logic for retrieve action
            return True
        return obj.status == "P"


class IsOrderItemByBuyer(BasePermission):
    """
    Check if order item is owned by appropriate buyer
    """

    def has_permission(self, request, view):
        order_id = view.kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        return order.buyer == request.user

    def has_object_permission(self, request, view, obj):
        return obj.order.buyer == request.user


class IsOrderByBuyer(BasePermission):
    """
    Check if order is owned by appropriate buyer
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user


class IsOrderItemPending(BasePermission):
    """
    Check the status of order is pending or completed before creating, updating and deleting order items
    """

    message = _(
        "Creating, updating or deleting order items for a closed order is not allowed."
    )

    def has_permission(self, request, view):
        order_id = view.kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id)

        if view.action in ("list",):
            return True

        return order.status == "P"

    def has_object_permission(self, request, view, obj):
        # if view.action in ("retrieve",):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.order.status == "P"



