# Generated by Django 3.2.9 on 2022-04-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_freelanceraccount_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelanceraccount',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
