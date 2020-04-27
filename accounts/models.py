from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField('닉네임', max_length=64, unique=True)
    profile_photo = models.ImageField()
    birthday = models.DateField('생일', blank=True, default='2020-01-01')    
    GENDER_CHOICES = [
        ('남', '남'),
        ('여', '여')
    ]
    gender = models.CharField('성별', max_length=2, choices=GENDER_CHOICES)
    host_introduce = models.TextField('호스트', blank=True)
    host_career = models.TextField('경력사항', blank=True)

    