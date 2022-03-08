# Generated by Django 3.2.9 on 2022-03-05 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220301_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='male', max_length=50),
        ),
        migrations.AlterField(
            model_name='freelanceraccount',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='male', max_length=50),
        ),
    ]