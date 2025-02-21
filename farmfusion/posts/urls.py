from django.urls import path
from .views import feed, add_post,like_post  # Import add_post

urlpatterns = [
    path('', feed, name='feed'),  # Homepage displaying posts
    path('add_post/', add_post, name='add_post'),  # New route for adding a post
    path('like_post/', like_post, name='like_post')
]
