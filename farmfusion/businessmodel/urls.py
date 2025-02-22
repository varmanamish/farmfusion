from django.urls import path
from . import views

urlpatterns = [
    path('myprojects/', views.myprojects, name='myprojects'),
    path('createinvestment/', views.createinvestmentmodel, name='createinvestmentmodel'), 
    path('showallmodels/', views.showallmodels, name='showallmodels'),
    path('invest/', views.invest, name='invest'),
    path("mlforms/", views.mlforms,name='mlforms')
]
