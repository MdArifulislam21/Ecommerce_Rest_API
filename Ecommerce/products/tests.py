from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, get_default_product_category, category_image_path, product_image_path


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')
        self.assertTrue(category.created_at is not None)
        self.assertTrue(category.updated_at is not None)

    def test_category_image_path(self):
        instance = Category(name='Test Category')
        filename = 'test_image.jpg'
        path = category_image_path(instance, filename)
        expected_path = f'category/icons/Test Category/{filename}'
        self.assertEqual(path, expected_path)


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')

    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            details='Test details',
            image='product_image.jpg',
            price=10.0,
            quantity=5,
            category=self.category,
            seller=self.user
        )
        self.assertEqual(str(product), 'Test Product')
        self.assertTrue(product.created_at is not None)
        self.assertTrue(product.updated_at is not None)

    def test_get_default_product_category(self):
        default_category = get_default_product_category()
        self.assertEqual(default_category.name, 'Others')

    def test_product_image_path(self):
        instance = Product(name='Test Product', category=self.category, seller=self.user)
        filename = 'test_image.jpg'
        path = product_image_path(instance, filename)
        expected_path = f'product/images/Test Product/{filename}'
        self.assertEqual(path, expected_path)