# Generated by Django 3.2.9 on 2022-07-03 06:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_auto_20220521_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='slug',
            field=models.SlugField(default=uuid.UUID('7b2bd226-1725-40a7-93c9-344cfdabddfc'), unique=True),
        ),
        migrations.AlterField(
            model_name='freelanceraccount',
            name='slug',
            field=models.SlugField(default=uuid.UUID('4b8f022a-4e16-4485-bd3f-745b69aa357e'), unique=True),
        ),
    ]