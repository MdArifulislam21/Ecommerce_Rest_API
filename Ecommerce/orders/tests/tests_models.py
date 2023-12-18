from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Order, OrderItem
from products.models import Category, Product  
# from .tests import get_or_create_category_and_product 


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category, self.product = get_or_create_category_and_product()

    def test_order_creation(self):
        order = Order.objects.create(buyer=self.user)
        self.assertEqual(str(order), self.user.get_full_name())
        self.assertEqual(order.status, Order.PENDING)
        self.assertTrue(order.created_at is not None)
        self.assertTrue(order.updated_at is not None)

    def test_order_total_cost(self):
        order = Order.objects.create(buyer=self.user)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=3)

        expected_total_cost = round(order_item.cost, 2)
        self.assertEqual(order.total_cost, expected_total_cost)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category, self.product = get_or_create_category_and_product()
        self.order = Order.objects.create(buyer=self.user)


    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(str(order_item), self.user.get_full_name())
        self.assertTrue(order_item.created_at is not None)
        self.assertTrue(order_item.updated_at is not None)


    def test_order_item_cost(self):
        quantity = 3
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=quantity)

        expected_cost = round(quantity * self.product.price, 2)
        self.assertEqual(order_item.cost, expected_cost)



def get_or_create_category_and_product():
    category = Category.objects.create(name='Test Category')
    product = Product.objects.create(name='Test Product', details='Test details', image='product_image.jpg',
                                     price=10.0, quantity=5, category=category, seller=User.objects.first())
    return category, product
