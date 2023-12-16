from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .views import PaymentViewSet
from orders.views import OrderViewSet
from .models import Payment

from .permissions import (
    IsPaymentByUser,
    IsPaymentPending,
    IsOrderPendingWhenCheckout,
)
     

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(buyer=self.user, status=Order.PENDING)
        self.payment = Payment.objects.create(order=self.order, status=Payment.PENDING)

    def test_is_payment_by_user_permission(self):
        view = PaymentViewSet.as_view({'get': 'retrieve'})
        request = APIRequestFactory().get("/payments/1/")
        request.user = self.user

        # Test that user can retrieve their own payment
        permission = IsPaymentByUser()
        self.assertTrue(permission.has_object_permission(request, view, self.payment))

        # Test that admin can retrieve any payment
        admin_user = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com')
        request.user = admin_user
        self.assertTrue(permission.has_object_permission(request, view, self.payment))

        # Test that user cannot retrieve someone else's payment
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        request.user = other_user
        self.assertFalse(permission.has_object_permission(request, view, self.payment))

    def test_is_payment_pending_permission(self):
        # factory = APIRequestFactory()
        view = PaymentViewSet.as_view({'get': 'retrieve'})
        request = APIRequestFactory().get("/payments/1/")
        request.user = self.user

        # Test that user can retrieve pending payment
        permission = IsPaymentPending()
        self.assertTrue(permission.has_object_permission(request, view, self.payment))

    def test_is_order_pending_when_checkout_permission(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'put': 'update'})
        request = factory.put('/orders/1/')
        request.user = self.user

        # Test that user can update a pending order during checkout
        permission = IsOrderPendingWhenCheckout()
        self.assertTrue(permission.has_object_permission(request, view, self.order))

        # Test that user cannot update a completed order during checkout
        self.order.status = Order.COMPLETED
        self.order.save()
        self.assertFalse(permission.has_object_permission(request, view, self.order))
