import uuid

from django.utils.timezone import now
from django.db import models

from users.models import User


class RefCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referral_code")
    created_at = models.DateTimeField(auto_now_add=True)
    ref_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"{self.user.user_name} - {self.ref_code}"
