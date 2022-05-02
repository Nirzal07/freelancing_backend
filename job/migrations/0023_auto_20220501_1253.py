# Generated by Django 3.2.9 on 2022-05-01 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0022_alter_job_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='listing_type',
            field=models.CharField(choices=[('free', 'Free'), ('standard', 'Standard'), ('premium', 'Premium')], default='free', max_length=20),
        ),
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('not_hired', 'Not Hired'), ('hired', 'Hired'), ('completed', 'Completed')], default='not_hired', max_length=20),
        ),
    ]