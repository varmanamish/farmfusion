from django.urls import path
from .views import feed, add_post

urlpatterns = [
    path('', feed, name='feed'),  # Homepage displaying posts
    path('add/', add_post, name='add_post'),  # Page to add posts
]
