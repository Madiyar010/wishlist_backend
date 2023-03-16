from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomAccountManager
import uuid


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default_profile_image.png')

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username
