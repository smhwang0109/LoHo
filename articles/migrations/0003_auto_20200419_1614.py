# Generated by Django 3.0.5 on 2020-04-19 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20200419_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='man_applicant',
            new_name='man_count',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='woman_applicant',
            new_name='woman_count',
        ),
    ]
