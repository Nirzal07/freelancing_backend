# Generated by Django 3.2.9 on 2022-04-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_freelanceraccount_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelanceraccount',
            name='slug',
            field=models.SlugField(default='aaaaa', unique=True),
            preserve_default=False,
        ),
    ]