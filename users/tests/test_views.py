from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class TestCustomRegisterView(APITestCase):

    def test_register_post(self):
        url = reverse('register')
        data = {
            'email': 'email@mail.ru',
            'username': 'username',
            'first_name': 'name',
            'password': '123fwefGG',
        }
        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
