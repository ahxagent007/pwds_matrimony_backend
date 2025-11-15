import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# ---------------------------
# Custom User Model
# ---------------------------
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)

    gender = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    device_id = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Pending", "Pending"),
            ("Suspended", "Suspended"),
            ("Deleted", "Deleted"),
        ],
        default="Pending"
    )

    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email


# ---------------------------
# Two-Factor Authentication
# ---------------------------
class TwoFactorAuth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="two_factor_codes")
    code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


# ---------------------------
# Admin Users
# ---------------------------
class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        choices=[("Moderator", "Moderator"), ("SuperAdmin", "SuperAdmin")]
    )

    def __str__(self):
        return f"{self.name} ({self.role})"


# ---------------------------
# Admin Activity Logs
# ---------------------------
class AdminLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name="logs")
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_actions")

    action = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
