from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('normal', 'Normal User'),
        ('verified', 'Verified User'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Following(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.follower.username + ' is following ' + self.following.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' token'
