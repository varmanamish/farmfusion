from django.urls import path
from . import views
from ecommerce.views import shop
from posts.views import feed
urlpatterns=[
    path('',views.index,name="index"),  
]