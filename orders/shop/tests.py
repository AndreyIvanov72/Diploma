from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, Contact, Category, ProductInfo
from .serializers import OrderSerializer, ContactSerializer, CategorySerializer, ProductSerializer
from unittest.mock import patch
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        self.client.force_authenticate(user=self.user)


def test_user_login_valid_credentials(self):
    user = User.objects.create_user(username='testuser', password='testpass')
    
    login_data = {
        'username': 'testuser',
        'password': 'testpass'
    }
    
    response = self.client.post('/api/login/', login_data, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    self.assertIn('refresh', response.data)
    self.assertIn('access', response.data)
    
    self.assertNotEqual(response.data['refresh'], '')
    self.assertNotEqual(response.data['access'], '')

def test_invalid_login_credentials(self):
    url = '/api/login/' 
    data = {'username': 'nonexistent_user', 'password': 'wrong_password'}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {'error': 'Invalid credentials'})

def test_product_list_view(self):
    ProductInfo.objects.create(name="Product 1", price=10.00)
    ProductInfo.objects.create(name="Product 2", price=20.00)

    response = self.client.get('/products/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

    self.client.force_authenticate(user=self.user)
    response = self.client.get('/products/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

def test_create_contact_authenticated_user(self):
    self.client.force_authenticate(user=self.user)
    contact_data = {
        'phone': '1234567890',
        'country': 'Test Country',
        'city': 'Test City',
        'street': 'Test Street',
        'house': '123'
    }
    
    with patch('shop.views.send_contact_confirmation_email.delay') as mock_send_email:
        response = self.client.post('/api/contacts/', contact_data)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Contact.objects.count(), 1)
    contact = Contact.objects.first()
    self.assertEqual(contact.user, self.user)
    self.assertEqual(contact.email, self.user.email)
    mock_send_email.assert_called_once_with(self.user.email)

def test_non_existent_product_detail(self):
    non_existent_product_id = 9999  # Assuming this ID doesn't exist
    response = self.client.get(f'/products/{non_existent_product_id}/')
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_create_order_authenticated_user(self):
    self.client.force_authenticate(user=self.user)
    order_data = {
        'items': [{'product': 1, 'quantity': 2}],
        'status': 'New'
    }
    response = self.client.post('/orders/', order_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Order.objects.count(), 1)
    self.assertEqual(Order.objects.get().user, self.user)

def test_order_confirmation(self):
    order = Order.objects.create(user=self.user, status='Pending')
    
    with patch('shop.views.send_order_confirmation_email.delay') as mock_send_email:
        response = self.client.post(f'/api/orders/{order.id}/confirm/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order confirmed')
        
        order.refresh_from_db()
        self.assertEqual(order.status, 'Confirmed')
        
        mock_send_email.assert_called_once_with(self.user.email)
    
def test_order_confirmation_unauthorized_user(self):
    user1 = User.objects.create_user(username='user1', password='pass1', email='user1@example.com')
    user2 = User.objects.create_user(username='user2', password='pass2', email='user2@example.com')

    order = Order.objects.create(user=user1, status='Pending')

    self.client.force_authenticate(user=user2)

    response = self.client.post(f'/orders/{order.id}/confirm/')

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data['message'], 'Нет доступа')

    order.refresh_from_db()
    self.assertEqual(order.status, 'Pending')