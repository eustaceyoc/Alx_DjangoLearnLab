from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='following_users',blank=True,symmetrical=False)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='follower_users',blank=True,symmetrical=False)