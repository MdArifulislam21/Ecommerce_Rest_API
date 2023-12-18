
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from products.models import Product, Category
from users.models import UserAddress

User = get_user_model()

class OrderWriteSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.use1 = User.objects.create_user(username='testuser1', password='testpass')
        self.address = UserAddress.objects.create(
            user=self.user,
            address_type=UserAddress.BILLING,
            default=False,
            country='US',
            city='City',
            street='Street',
            apartment='Apt 1',
            postal_code='12345'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', seller=self.use1 , category=self.category, price=10.0, quantity=50)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_order_with_order_items(self):
        order_items_data = [
            {'product': self.product.id, 'quantity': 2},
            {'product': self.product.id, 'quantity': 3}
        ]

        data = {
            'buyer': self.user.id,
            'status': Order.PENDING,
            'order_items': order_items_data
        }

        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_update_order_with_order_items(self):
        order = Order.objects.create(buyer=self.user, status=Order.PENDING)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)

        updated_order_items_data = [
            {'product': self.product.id, 'quantity': 3}
        ]

        updated_data = {
            'order_items': updated_order_items_data
        }

        url = f'/api/orders/{order.id}/'
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 3)

    def test_create_order_with_insufficient_product_quantity(self):
        self.product.quantity = 1  # product quantity less than ordered quantity
        self.product.save()

        order_items_data = [
            {'product': self.product.id, 'quantity': 2},
        ]

        data = {
            'buyer': self.user.id,
            'status': Order.PENDING,
            'order_items': order_items_data
        }

        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

