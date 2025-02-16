from django.urls import path
from .views import socialmedia_view    

urlpatterns = [
    path('', socialmedia_view, name='socialmedia'),  
]
