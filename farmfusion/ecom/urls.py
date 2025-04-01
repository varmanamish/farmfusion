from django.urls import path
from . import views
from ecommerce.views import shop
from posts.views import feed
from support.views import support_posts
urlpatterns=[
    path('',views.index,name="index"),
    path('feed', feed, name="feed"),
    path('shop', shop, name="shop"),
    path('contacts', views.contacts, name="contacts"),
    path('partners', views.partners, name="partners"),
    path('privacy', views.privacy, name="privacy"),
    path('support/',support_posts,name="support"),
]