# Generated by Django 3.2.9 on 2022-04-25 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20220423_1226'),
        ('job', '0018_proposal_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.freelanceraccount'),
        ),
    ]
