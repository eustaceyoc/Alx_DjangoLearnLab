from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Step 1a: Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password=password, **extra_fields)

# Step 1b: Custom user model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.CharField(max_length=255, null=True, blank=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username
