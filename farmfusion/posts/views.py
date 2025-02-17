from django.shortcuts import render, redirect
from .models import postdetails as Post

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})

def add_post(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        location = request.POST.get('location', '')  
        caption = request.POST.get('caption', '')
        profile_pic = request.FILES.get('profile_pic')
        post_image = request.FILES.get('post_image')

        # Ensure files are uploaded properly
        if profile_pic:
            profile_pic.name = f"profile_{username}_{profile_pic.name}"
        if post_image:
            post_image.name = f"post_{username}_{post_image.name}"

        # Create and save the post
        Post.objects.create(
            username=username,
            location=location,
            caption=caption,
            profile_pic=profile_pic,
            post_image=post_image,
            likes_count=0  
        )

        return redirect('feed')  # Redirect to the feed page after posting
