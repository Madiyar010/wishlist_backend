# Generated by Django 4.1.7 on 2023-03-15 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0005_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
