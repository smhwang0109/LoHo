from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64, unique=True)
    profile_photo = models.ImageField(default='accounts/static/accounts/img/수민사진.jpg')
    GENDER_CHOICES = [
        ('남', '남'),
        ('여', '여')
    ]
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    host_introduce = models.TextField(blank=True)
    host_career = models.TextField(blank=True)

    