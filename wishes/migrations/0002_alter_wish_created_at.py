# Generated by Django 4.1.7 on 2023-03-18 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
