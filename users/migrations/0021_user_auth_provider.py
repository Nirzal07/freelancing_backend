# Generated by Django 3.2.9 on 2022-04-12 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_remove_user_auth_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(default='custom', max_length=255),
        ),
    ]
