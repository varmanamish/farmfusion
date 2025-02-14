from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('/products', views.products, name="products"),
    path('/services', views.services, name="services"),
    path('/contacts', views.contacts, name="contacts"),
    path('/partners', views.partners, name="partners"),
    path('/privacy', views.privacy, name="privacy"),
]