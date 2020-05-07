from django.db import models
from django.utils import timezone
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.conf import settings


def unit_100(value):
    if value%100:
        raise forms.ValidationError('100원 단위로 입력해주세요.')

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}.{}'.format(instance.author.username, pid, extension)

class Article(models.Model):
    title = models.CharField('제목', max_length=126, validators=[MinLengthValidator(1)])
    content = models.TextField('내용', validators=[MinLengthValidator(1)])
    to_who = models.TextField('대상', default='')
    detail_plan = models.TextField('상세 일정', default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE)
    price = models.IntegerField(
        '가격',
        default=1000,
        validators=[
            MinValueValidator(1000),
            unit_100,
        ])
    participations = models.IntegerField(
        '참가 가능 인원',
        default=1,
        validators=[
            MinValueValidator(1),
        ])
    man_participations = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='man_participations',
        through='ManParticipation',
        )
    woman_participations = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='woman_participations',
        through='WomanParticipation',
        )
    event_date = models.DateTimeField('날짜')
    image = models.ImageField(upload_to=user_path, default='')
    thumnail_image = models.ImageField(blank=True)
    CATEGORY_CHOICES = [
        ('스포츠', '스포츠'),
        ('이색체험', '이색체험'),
        ('쿠킹', '쿠킹'),
        ('예술', '예술'),
        ('관람', '관람'),
        ('기타', '기타'),
    ]
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, default='')
    created_at = models.DateTimeField('작성시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정시간', auto_now=True)
    

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)

    @property
    def man_participations_count(self):
        return self.man_participations.count()
    
    @property
    def woman_participations_count(self):
        return self.woman_participations.count()

class ManParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'article')
        )

class WomanParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'article')
        )

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    rank = models.IntegerField(
        '평점',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        )
    content = models.TextField('내용', validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField('작성시간', auto_now_add=True)
    updated_at = models.DateTimeField('수정시간', auto_now=True)