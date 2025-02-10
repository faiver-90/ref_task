import uuid

from django.db import models
from django.utils.timezone import now


class User(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=256, unique=True, blank=True, null=True)
    refresh_token = models.CharField(max_length=256, unique=True, blank=True, null=True)
    role = models.CharField(max_length=256, blank=True, null=True)
    self_ref_code = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.user_name


class RefCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referral_code")
    created_at = models.DateTimeField(auto_now_add=True)
    ref_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"{self.user.user_name} - {self.ref_code}"