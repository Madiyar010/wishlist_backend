import pytest
from wishes.models import Wish
from users.models import Account


@pytest.fixture()
def wish(db):
    test_wish = Wish.objects.create(
        owner=user,
        name='wish_name',
    )
    return test_wish


@pytest.fixture()
def user(db):
    test_user = Account.objects.create_user(
        email='new@mail.ru',
        username='new_user',
        password='12345678Qa'
    )
    return test_user
