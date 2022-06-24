import jwt

from datetime import datetime, timedelta
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from CoreApp import settings


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, role=None, title=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        if username is None:
            raise TypeError('Users must have an username')

        user = self.model(username=username, email=self.normalize_email(email), title=title, role=role)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=255, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def access_token(self):
        return self._generate_access_jwt_token()

    @property
    def set_and_get_refresh_token(self):
        refresh_token = self._generate_refresh_token()
        self.refresh_token = refresh_token
        self.save()
        return refresh_token

    def update_refresh_token(self):
        self.refresh_token = self._generate_refresh_token()
        self.save()

    def _generate_access_jwt_token(self):
        dt = datetime.now() + timedelta(minutes=5)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def _generate_refresh_token(self):
        dt = datetime.now() + timedelta(hours=5)

        token = jwt.encode({
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token




