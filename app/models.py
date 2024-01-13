from django.contrib.auth.models import User
from django.db import models


class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='Користувач')
    is_checked = models.BooleanField(default=False, verbose_name='is_checked')

    def __str__(self):
        return f'{self.user}'
