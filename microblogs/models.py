from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ symbol followed by at least 3 alphanumericals'
        )]
    )

    first_name = models.CharField(
        max_length=50,
        unique=False,
        blank=False
    )

    last_name = models.CharField(
        max_length=50,
        unique=False,
        blank=False
    )

    email = models.EmailField(
        unique=True,
        blank=False
    )

    bio = models.CharField(
        max_length=520,
        blank=True
    )

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        blank=False
    )
    
    text = models.CharField(
        max_length=280,
        unique=False,
        blank=False
    )
    
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]