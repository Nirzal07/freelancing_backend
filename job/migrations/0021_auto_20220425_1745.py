# Generated by Django 3.2.9 on 2022-04-25 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20220423_1226'),
        ('job', '0020_auto_20220425_1342'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together={('job', 'proposant')},
        ),
        migrations.CreateModel(
            name='JobRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.freelanceraccount')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
            ],
            options={
                'verbose_name': 'Job Request',
                'verbose_name_plural': 'Job Requests',
                'unique_together': {('job', 'freelancer')},
            },
        ),
    ]
