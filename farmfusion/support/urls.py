from django.urls import path
from .views import support_posts

urlpatterns = [
    path('', support_posts, name='support_posts'),
]
