# support/models.py

from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model from the accounts app

class SupportPost(models.Model):
    requesting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_requests')
    requested_support_amount = models.IntegerField()
    sponsoring_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='sponsored_support_posts')
    finished = models.BooleanField(default=False)
    support_image = models.ImageField(upload_to='support_posts/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Support request by {self.requesting_user.username} for {self.requested_support_amount}"
