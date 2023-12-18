from django.test import TestCase
from orders.models import Order
from orders.permissions import IsOrderPending
from users.models import User
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from orders.models import Order, OrderItem
from orders.permissions import IsOrderItemByBuyer, IsOrderByBuyer
from products.models import Category, Product


class IsOrderPendingTests(TestCase):
    """"
    This test checks if orderitem can be updated or deleted , when it is in pending state.
    And when it is completed state.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(buyer=self.user, status="P")
        self.order1 = Order.objects.create(buyer=self.user, status="C")

    def test_update_non_pending_order(self):

        request = APIRequestFactory().put("/orders/1/", data={})
        request.user = self.user

        permission = IsOrderPending()
        self.assertFalse(permission.has_object_permission(request, None, self.order1))

    def test_delete_non_pending_order(self):
        request = APIRequestFactory().delete("/orders/1/")
        request.user = self.user

        permission = IsOrderPending()
        self.assertFalse(permission.has_object_permission(request, None, self.order1))

    def test_update_pending_order(self):
        request = APIRequestFactory().put("/orders/1/", data={})
        request.user = self.user

        permission = IsOrderPending()
        self.assertTrue(permission.has_object_permission(request, None, self.order))

    def test_delete_pending_order(self):
        request = APIRequestFactory().delete("/orders/1/")
        request.user = self.user

        permission = IsOrderPending()
        self.assertTrue(permission.has_object_permission(request, None, self.order))


class IsOrderByBuyerTests(TestCase):
    """
    This testcase check access of orders buyer.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.order = Order.objects.create(buyer=self.user, status="P")
        
    def test_unauthorized_access(self):
        request = APIRequestFactory().get("/orders/1/items/1/")
        request.user = self.user2

        permission = IsOrderByBuyer()
        self.assertFalse(permission.has_object_permission(request, None, self.order))


    def test_authorized_access(self):
        request = APIRequestFactory().get("/orders/1/items/1/")
        request.user = self.user

        permission = IsOrderByBuyer()
        self.assertTrue(permission.has_object_permission(request, None, self.order))
    



class IsOrderItemByBuyerTests(TestCase):
    """
    This testcase check access of order items buyer.
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            details='Test details',
            image='product_image.jpg',
            price=10.0,
            quantity=5,
            category=self.category,
            seller=self.user1
        )
        self.order = Order.objects.create(buyer=self.user1, status=Order.PENDING)
        self.order_item = OrderItem.objects.create(order=self.order, quantity=1, product=self.product)

    def test_unauthorized_access(self):

        request = APIRequestFactory().get("/orders/1/items/1/")
        request.user = self.user2

        permission = IsOrderItemByBuyer()
        self.assertFalse(permission.has_object_permission(request, None, self.order_item))

    def test_authorized_access(self):
        request = APIRequestFactory().get("/orders/1/items/1/")
        request.user = self.user1

        permission = IsOrderItemByBuyer()
        self.assertTrue(permission.has_object_permission(request, None, self.order_item))
   