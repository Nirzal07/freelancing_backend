# Generated by Django 3.2.9 on 2022-05-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_alter_freelanceraccount_portfolios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelanceraccount',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freelanceraccount',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=50, null=True),
        ),
    ]
