from django.urls import path
from . import views
from ecommerce.views import shop
from posts.views import feed
urlpatterns=[
    path('',views.index,name="index"),
    path('feed', feed, name="feed"),
    path('shop', shop, name="shop"),
    path('contacts', views.contacts, name="contacts"),
    path('partners', views.partners, name="partners"),
    path('privacy', views.privacy, name="privacy"),
    
]