# Generated by Django 3.2.9 on 2022-04-12 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_user_auth_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='registered_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='freelanceraccount',
            name='registered_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]