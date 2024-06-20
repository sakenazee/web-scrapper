from django.test import TestCase
from scrapper.models import Product, Brand
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ProductModelTest(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name="Test Brand")

    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product",
            asin="B001234567",
            sku="SKU123",
            image="http://example.com/image.jpg",
            brand=self.brand
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.asin, "B001234567")
        self.assertEqual(product.sku, "SKU123")
        self.assertEqual(product.image, "http://example.com/image.jpg")
        self.assertEqual(product.brand, self.brand)

    def test_unique_asin(self):
        Product.objects.create(
            name="Product1",
            asin="B001234567",
            sku="SKU123",
            image="http://example.com/image1.jpg",
            brand=self.brand
        )
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Product2",
                asin="B001234567",  # Duplicate ASIN should raise an error
                sku="SKU124",
                image="http://example.com/image2.jpg",
                brand=self.brand
            )


class ProductViewSetTest(APITestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name="Test Brand")
        self.product = Product.objects.create(
            name="Test Product",
            asin="B001234567",
            sku="SKU123",
            image="http://example.com/image.jpg",
            brand=self.brand
        )

    def test_list_products(self):
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Product')

    def test_get_brand_products(self):
        url = reverse('brand-product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Test Brand')
        self.assertEqual(len(response.data[0]['products']), 1)


from django.test import TestCase
from scrapper.models import Product, Brand
from scrapper.tasks import scrape_all_brands
from unittest.mock import patch

class ScrapeTaskTest(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name="Test Brand")

    @patch('scrapper.tasks.scrape_amazon_brand')
    def test_scrape_all_brands(self, mock_scrape_amazon_brand):
        scrape_all_brands()
        self.assertTrue(mock_scrape_amazon_brand.called)
        self.assertEqual(mock_scrape_amazon_brand.call_count, 1)


from django.test import TestCase
from scrapper.models import Product, Brand
from scrapper.serializers import ProductSerializer, BrandSerializer

class ProductSerializerTest(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name="Test Brand")
        self.product = Product.objects.create(
            name="Test Product",
            asin="B001234567",
            sku="SKU123",
            image="http://example.com/image.jpg",
            brand=self.brand
        )

    def test_product_serializer(self):
        serializer = ProductSerializer(self.product)
        self.assertEqual(serializer.data['name'], 'Test Product')
        self.assertEqual(serializer.data['asin'], 'B001234567')
        self.assertEqual(serializer.data['brand'], self.brand.id)

    def test_brand_serializer(self):
        serializer = BrandSerializer(self.brand)
        self.assertEqual(serializer.data['name'], 'Test Brand')
        self.assertEqual(len(serializer.data['products']), 1)
        self.assertEqual(serializer.data['products'][0]['name'], 'Test Product')
