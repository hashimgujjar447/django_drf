from django.test import TestCase
from api.models import Order,User
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserOrderTestClass(TestCase):
    def setUp(self):
        user1=User.objects.create_user(username="awais",password="awais1234")
        user2=User.objects.create_user(username="umair",password="umair1234")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)
    def test_user_order_endpoint_retrieve_only_authenticated_user_orders(self):
        user=User.objects.get(username="awais")
        self.client.force_login(user)

        response=self.client.get(reverse('user_orders'))

        assert response.status_code == 200
        orders=response.json()
        self.assertTrue(all(order['user']['id'] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        response=self.client.get(reverse('user_orders'))
        self.assertEqual(response.status_code,401)