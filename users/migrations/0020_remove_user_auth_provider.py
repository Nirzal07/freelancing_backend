# Generated by Django 3.2.9 on 2022-04-12 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_freelanceraccount_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auth_provider',
        ),
    ]
