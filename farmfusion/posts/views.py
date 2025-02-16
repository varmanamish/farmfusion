from django.shortcuts import render
from .models import Post
from .forms import PostForm  # Make sure this line is added
from django.shortcuts import render, redirect  # Add redirect here


def feed(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts, newest first
    return render(request, 'posts/feed.html', {'posts': posts})


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed')  # Redirect to the feed page
    else:
        form = PostForm()
    return render(request, 'posts/add_post.html', {'form': form})
