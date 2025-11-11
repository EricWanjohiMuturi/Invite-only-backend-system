from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    USER_ROLES = (
    ('admin', 'Admin'),
    ('director', 'Director'),
    ('marketing', 'MarketingManager'),
    ('inventory', 'InventoryManager'),
    ('accountant', 'Accountant'),
    ('sales', 'SalesRepresentative'),
    )


    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=USER_ROLES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # email is required (USERNAME_FIELD)


    def __str__(self):
        return f"{self.email} ({self.role})"




class Invitation(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()
    role = models.CharField(max_length=32, choices=CustomUser.USER_ROLES)
    invited_by = models.ForeignKey('CustomUser', null=True, on_delete=models.SET_NULL, related_name='sent_invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        indexes = [models.Index(fields=['email']), models.Index(fields=['token'])]


    def is_expired(self):
        return timezone.now() > self.expires_at


    def mark_accepted(self):
        self.accepted = True
        self.accepted_at = timezone.now()
        self.save()

class PasswordResetRequest(models.Model):
    def expire_in_20_minutes():
        return timezone.now() + timedelta(minutes=20)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=expire_in_20_minutes)

    def __str__(self):
        return f"Password reset request for {self.user.email}"

    # <-- Add this method
    def is_expired(self):
        return timezone.now() > self.expires_at
