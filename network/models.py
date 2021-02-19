from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    age = models.CharField(verbose_name='Age', max_length=64, null=True, blank=True)
    SEX = (
        (1, 'Woman'),
        (2, 'Man'),
        (3, 'Undefined'),

    )
    sex = models.IntegerField(verbose_name='SEX', choices=SEX)
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Post(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='User', on_delete=models.CASCADE)
    text = models.CharField(max_length=512)


class Like(models.Model):
    LIKE = (
        ('like', 'like'),
        ('dislike', 'dislike')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like = models.CharField(max_length=255, choices=LIKE)
    date = models.DateField(auto_now=True)
