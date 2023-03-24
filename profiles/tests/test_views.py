from rest_framework.test import APITestCase
from users.models import Account
from wishes.models import Wish
from django.urls import reverse
from rest_framework import status


class TestProfileViewSet(APITestCase):
    def setUp(self):
        self.owner = Account.objects.create_user(
            username='new_user',
            first_name='name',
            email='new@mail.ru',
            password='123EDF2s',
        )
        self.user = Account.objects.create_user(
            username='n_user',
            first_name='name',
            email='neww@mail.ru',
            password='123EDF2s',
        )
        self.client.force_authenticate(user=self.user)
        self.wish = Wish.objects.create(
            id='0508eecd-0cf1-4b9e-ae58-ec171f7ed1ae',
            owner=self.owner,
            name='My wish',
        )

    def test_update_request_like_wish(self):
        url = reverse('Profiles-detail', args=[self.wish.id])
        response = self.client.put(url)
        self.assertEqual(response.json(), {'message': 'wish liked'})

    def test_update_request_unlike_wish(self):
        self.wish.liked_by = self.user
        self.wish.save()
        url = reverse('Profiles-detail', args=[self.wish.id])
        response = self.client.put(url)
        self.assertEqual(response.json(), {'message': 'like removed'})

    def test_update_request_not_allowed(self):
        self.wish.owner = self.user
        self.wish.save()
        url = reverse('Profiles-detail', args=[self.wish.id])
        response = self.client.put(url)
        self.assertEqual(response.json(), {'message': 'not allowed'})

    def test_list_request(self):
        url = reverse('Profiles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_request(self):
        url = reverse('Profiles-detail', args=[self.owner.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
