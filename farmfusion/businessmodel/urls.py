from django.urls import path
from . import views

urlpatterns = [
    path('myinvestment/', views.myinvestment, name="myinvestment"),
    path('myprojects/', views.myprojects, name='myprojects'),
    path('createinvestment/', views.createinvestmentmodel, name='createinvestmentmodel'),  # New endpoint for form submission
]
