from django.db import models
from django.conf import settings
import uuid


class Wish(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)
    # links - DONT FORGET ABOUT THIS!!
    image = models.ImageField(upload_to='images/', default='images/default.png')
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True, blank=True,
                                 related_name='liked_by')

    def __str__(self):
        return self.name


class Image(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, related_name='wish')
    image = models.ImageField()
