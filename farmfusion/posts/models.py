from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model

class PostDetails(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    username = models.CharField(max_length=255, default='Anonymous')  # Ensure default value is set
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    post_image = models.ImageField(upload_to='post_images/')
    caption = models.TextField(blank=True)
    likes_count = models.IntegerField(default=0)

