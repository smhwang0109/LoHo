# Generated by Django 2.1.15 on 2020-04-23 08:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0004_auto_20200423_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='평점')),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(1)], verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='detail_plan',
            field=models.TextField(default='', verbose_name='상세 일정'),
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.Article'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
