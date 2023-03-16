from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    target = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='target')

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='from_user', null=True, blank=True)

    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.message

    def get_content_object_type(self):
        return str(self.content_object.get_cname)
