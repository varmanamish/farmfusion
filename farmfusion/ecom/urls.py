from django.urls import path
from . import views
from ecommerce.views import shop
from posts.views import feed
from support.views import support_posts
from businessmodel.views import submit_verification,verification_dashboard,approve_verification
urlpatterns=[
    path('',views.index,name="index"),
    path('feed', feed, name="feed"),
    path('shop', shop, name="shop"),
    path('contacts', views.contacts, name="contacts"),
    path('partners', views.partners, name="partners"),
    path('privacy', views.privacy, name="privacy"),
    path('support/',support_posts,name="support"),
    path('submit_verification/',submit_verification,name="submit_verification"),
    path('verification-dashboard/', verification_dashboard, name='verification_dashboard'),
    path('approve-verification/<int:verification_id>/<str:action>/',approve_verification, name='approve_verification'),
]