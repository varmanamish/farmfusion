from django.urls import path
from ecom.views  import index
from ecommerce.views import shop
from posts.views import feed
urlpatterns=[
    path('',index,name="index"),  
]