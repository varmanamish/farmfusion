from django.shortcuts import render, redirect
from .models import PostDetails as Post, Follow
from django.contrib.auth.decorators import login_required

def feed(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        followers = Follow.objects.filter(following=request.user)
        following = Follow.objects.filter(follower=request.user)
    else:
        followers = []
        following = []

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'followers': followers,
        'following': following
    })



# @login_required  # Ensure only logged-in users can post
def add_post(request):
    if request.method == 'POST':
        location = request.POST.get('location', '')  
        caption = request.POST.get('caption', '')
        profile_pic = request.FILES.get('profile_pic')
        post_image = request.FILES.get('post_image')

        # Ensure files are uploaded properly
        if profile_pic:
            profile_pic.name = f"profile_{request.user.username}_{profile_pic.name}"
        if post_image:
            post_image.name = f"post_{request.user.username}_{post_image.name}"

        # Create and save the post
        Post.objects.create(
            user=request.user,  # Automatically assign the logged-in user
            username=request.user.username,  # Save the username in the post
            profile_pic=request.user.profile_pic,  # Save the user's profile picture in the post
            location=location,
            caption=caption,
            post_image=post_image,
            likes_count=0  
        )

        return redirect('feed')  # Redirect to the feed page after posting

    return render(request, 'posts/add_post.html')  # Render form if GET request



