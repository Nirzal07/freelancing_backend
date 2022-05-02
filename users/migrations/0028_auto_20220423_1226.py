# Generated by Django 3.2.9 on 2022-04-23 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelanceraccount',
            name='portfolios',
            field=models.ManyToManyField(to='users.Portfolio'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freelaner_account', to='users.freelanceraccount'),
        ),
    ]
