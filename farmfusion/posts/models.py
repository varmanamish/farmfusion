from django.db import models

class Post(models.Model):
    username = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    post_image = models.ImageField(upload_to='post_images/')
    caption = models.TextField(blank=True)
    likes_count = models.IntegerField(default=0)
