# Generated by Django 3.2.9 on 2022-03-05 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220301_1521'),
        ('job', '0007_rename_applicants_proposals_proposants'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AppliedJobs',
            new_name='ProposedJobs',
        ),
    ]