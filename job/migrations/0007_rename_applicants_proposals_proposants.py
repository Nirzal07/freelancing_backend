# Generated by Django 3.2.9 on 2022-03-05 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_auto_20220305_0607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposals',
            old_name='applicants',
            new_name='proposants',
        ),
    ]
