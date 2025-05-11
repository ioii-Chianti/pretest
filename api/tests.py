from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.url = '/api/import-order/'
        self.valid_token = 'omni_pretest_token'
        self.valid_order_data = {
            'token': self.valid_token,
            'order_number': 'ORD123',
            'total_price': '100.50'
        }

    def test_create_order_successfully(self):
        response = self.client.post(self.url, self.valid_order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_missing_token(self):
        data = self.valid_order_data.copy()
        data.pop('token')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid token", response.content.decode())

    def test_invalid_token(self):
        data = self.valid_order_data.copy()
        data['token'] = 'wrong_token'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid token", response.content.decode())

    def test_missing_order_number(self):
        data = self.valid_order_data.copy()
        data.pop('order_number')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing", response.content.decode())

    def test_missing_total_price(self):
        data = self.valid_order_data.copy()
        data.pop('total_price')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing", response.content.decode())

    def test_invalid_total_price_format(self):
        data = self.valid_order_data.copy()
        data['total_price'] = 'abc'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid total_price format", response.content.decode())

    def test_duplicate_order_number(self):
        self.client.post(self.url, self.valid_order_data)
        response = self.client.post(self.url, self.valid_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Failed to create order", response.content.decode())