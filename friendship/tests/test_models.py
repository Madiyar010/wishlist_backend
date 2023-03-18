from rest_framework.test import APITestCase
from users.models import Account
from friendship.models import FriendList, FriendRequest


class FriendsListModelTestCase(APITestCase):
    def setUp(self):
        self.first_user = Account.objects.create_user(
            username='new_user',
            first_name='name',
            email='new@mail.ru',
            password='123EDF2s',
        )
        self.second_user = Account.objects.create_user(
            username='second_user',
            first_name='second_name',
            email='second@mail.ru',
            password='123EDF2s',
        )
        self.first_friend_list = FriendList.objects.get(user=self.first_user)
        self.second_friend_list = FriendList.objects.get(user=self.second_user)
        self.client.force_authenticate(user=self.first_user)

    def test_return_str(self):
        self.assertEqual(str(self.first_friend_list), self.first_user.username)

    def test_add_friend_method(self):
        self.first_friend_list.add_friend(self.second_user)
        self.assertEqual(len(self.first_friend_list.friends.all()), 1)
        self.assertEqual(len(self.second_friend_list.friends.all()), 1)

    def test_remove_friend_method(self):
        self.first_friend_list.add_friend(self.second_user)
        self.first_friend_list.remove_friend(self.second_user)
        self.assertEqual(len(self.first_friend_list.friends.all()), 0)
        self.assertEqual(len(self.second_friend_list.friends.all()), 0)

    def test_unfriend_method(self):
        self.first_friend_list.add_friend(self.second_user)
        self.first_friend_list.unfriend(self.second_user)
        friend_request = FriendRequest.objects.get(sender=self.second_user,
                                                   receiver=self.first_user,
                                                   )

        self.assertEqual(friend_request.is_active, True)

    def test_are_friends_method(self):
        self.first_friend_list.add_friend(self.second_user)
        self.assertEqual(self.first_friend_list.are_friends(self.second_user), True)
        self.first_friend_list.unfriend(self.second_user)
        self.assertEqual(self.first_friend_list.are_friends(self.second_user), False)

    def test_get_cname_property(self):
        self.assertEqual(self.first_friend_list.get_cname, 'FriendList')


class FriendRequestModelTestCase(APITestCase):
    def setUp(self):
        self.first_user = Account.objects.create_user(
            username='new_user',
            first_name='name',
            email='new@mail.ru',
            password='123EDF2s',
        )
        self.second_user = Account.objects.create_user(
            username='second_user',
            first_name='second_name',
            email='second@mail.ru',
            password='123EDF2s',
        )
        self.first_friend_request = FriendRequest.objects.create(
            sender=self.first_user,
            receiver=self.second_user,
        )

    def test_return_str(self):
        self.assertEqual(str(self.first_friend_request), self.first_user.username)

    def test_accept_method_is_active(self):
        self.first_friend_request.accept()
        self.assertEqual(self.first_friend_request.is_active, False)

