from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Extends built-in User model of Django. """

    def __str__(self):
        return self.username
