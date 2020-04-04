# Generated by Django 3.0.5 on 2020-04-04 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200404_1412'),
        ('articles', '0002_auto_20200404_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='accounts.Profile', to_field='nickname'),
        ),
    ]
