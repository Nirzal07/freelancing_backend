# Generated by Django 3.2.9 on 2022-03-28 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220308_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientaccount',
            old_name='gende',
            new_name='gender',
        ),
    ]
