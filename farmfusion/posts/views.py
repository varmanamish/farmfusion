from django.shortcuts import render
from .models import postdetails as Post
from django.shortcuts import render, redirect  # Add redirect here


def feed(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts, newest first
    return render(request, 'posts/feed.html', {'posts': posts})

