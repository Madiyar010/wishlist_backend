from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from users.models import Account


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user_id, timestamp):
        user = Account.objects.get(pk=user_id)
        return (
            six.text_type(user_id) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
