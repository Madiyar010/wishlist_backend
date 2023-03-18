from rest_framework.test import APITestCase
from users.models import Account
from wishes.models import Wish
from django.urls import reverse
from rest_framework import status


class WishViewTestCase(APITestCase):
    def setUp(self):
        self.owner = Account.objects.create_user(
            username='new_user',
            first_name='name',
            email='new@mail.ru',
            password='123EDF2s',
        )
        self.client.force_authenticate(user=self.owner)
        self.wish = Wish.objects.create(
            id='0508eecd-0cf1-4b9e-ae58-ec171f7ed1ae',
            owner=self.owner,
            name='My wish',
        )
        self.new_user = Account.objects.create_user(
            username='second_user',
            first_name='name',
            email='second@mail.ru',
            password='123EDF2s',
        )

    def test_get_queryset_authenticated_user(self):
        url = reverse('Wishes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_queryset_no_wishes(self):
        self.client.force_authenticate(user=self.new_user)
        url = reverse('Wishes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_queryset_unauthenticated_user(self):
        self.client.logout()
        url = reverse('Wishes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_wish(self):
        url = reverse('Wishes-list')
        data = {
            'name': 'wish_2',

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_wish(self):
        url = reverse('Wishes-list')
        data = {
            'name1': 'wef',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_wish(self):
        url = reverse('Wishes-detail', args=[self.wish.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_invalid_wish(self):
        url = reverse('Wishes-detail', args=[self.wish.pk])
        self.client.force_authenticate(user=self.new_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_wish(self):
        url = reverse('Wishes-detail', args=[self.wish.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_wishes(self):
        url = reverse('search_wishes', args=['книга'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

