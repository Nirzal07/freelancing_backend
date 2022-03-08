# Generated by Django 3.2.9 on 2022-03-01 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220301_1521'),
        ('job', '0003_auto_20220228_1422'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='District',
            new_name='Address',
        ),
        migrations.RemoveField(
            model_name='job',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='job',
            name='client',
        ),
        migrations.AddField(
            model_name='job',
            name='price',
            field=models.CharField(default='1000', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='price_is_range',
            field=models.BooleanField(default=True),
        ),
    ]