from django.test import TestCase
from django.contrib.auth.models import User
from products.models import TimestampedModel
from orders.models import Order
from ..models import Payment

class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(buyer=self.user, status=Order.PENDING)

    def test_payment_model(self):
        payment = Payment.objects.create(
            status=Payment.COMPLETED,
            payment_option=Payment.PAYPAL,
            order=self.order
        )

        # Test the default values
        self.assertEqual(payment.status, Payment.COMPLETED)
        self.assertEqual(payment.payment_option, Payment.PAYPAL)
        self.assertEqual(payment.order, self.order)

        # Test the ordering
        another_order = Order.objects.create(buyer=self.user, status=Order.PENDING)
        another_payment = Payment.objects.create(
            status=Payment.PENDING,
            payment_option=Payment.BKASH,
            order=another_order
        )

        # Payments should be ordered by the created_at field in descending order
        payments = Payment.objects.all()
        self.assertEqual(payments[0], another_payment)
        self.assertEqual(payments[1], payment)

 
