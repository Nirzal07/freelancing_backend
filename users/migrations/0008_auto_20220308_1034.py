# Generated by Django 3.2.9 on 2022-03-08 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_field_freelanceraccount_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientaccount',
            old_name='gender',
            new_name='gende',
        ),
        migrations.AlterField(
            model_name='clientaccount',
            name='contact',
            field=models.IntegerField(blank=True),
        ),
    ]