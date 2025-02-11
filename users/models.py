from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True, blank=True, null=True)
    token = models.CharField(max_length=256, unique=True, blank=True, null=True)
    refresh_token = models.CharField(max_length=256, unique=True, blank=True, null=True)
    role = models.CharField(max_length=256, blank=True, null=True)
    invite_ref_code = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.user_name
