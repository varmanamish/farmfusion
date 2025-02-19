from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
          # Automatically create a wallet for the user
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='pics', null=True, blank=True)
    is_farmer = models.BooleanField(default=False)
    dob = models.DateField(default=timezone.now)
    phno = models.CharField(max_length=15, default='000000000')  # Added max_length
    objects = CustomUserManager()  # Use custom manager

    def __str__(self):
        return self.username

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")
    wallet_pin =models.CharField(null=True)
    wallet_amount = models.IntegerField(default=0)
    free_amount = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Wallet"
