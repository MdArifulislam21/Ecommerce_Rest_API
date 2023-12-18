from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, UserAddress


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile =self.user.profile

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertTrue(self.profile.created_at <= timezone.now())
        self.assertTrue(self.profile.updated_at <= timezone.now())
        self.assertEqual(str(self.profile), self.user.get_full_name())


class UserAddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
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

    def test_address_creation(self):
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.address_type, UserAddress.BILLING)
        self.assertFalse(self.address.default)
        self.assertEqual(self.address.country.code, 'US')
        self.assertEqual(self.address.city, 'City')
        self.assertEqual(self.address.street, 'Street')
        self.assertEqual(self.address.apartment, 'Apt 1')
        self.assertEqual(self.address.postal_code, '12345')
        self.assertTrue(self.address.created_at <= timezone.now())
        self.assertTrue(self.address.updated_at <= timezone.now())

    def test_address_str_method(self):
        expected_str = f"{self.user.get_full_name()}"
        self.assertEqual(str(self.address), expected_str)