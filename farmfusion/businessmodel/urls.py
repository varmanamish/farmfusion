from django.urls import path
from . import views

urlpatterns = [
    path('myprojects/', views.myprojects, name='myprojects'),
    path('createinvestment/', views.createinvestmentmodel, name='createinvestmentmodel'), 
    path('showallmodels/', views.showallmodels, name='showallmodels'),
    path('invest/', views.invest, name='invest'),
    path("mlforms/", views.mlforms,name='mlforms'),
    path('raisequery/',views.raise_verification_query,name="raisequery"),
    path('submit_verification/',views.submit_verification,name="submit_verification"),
    path('verification-dashboard/', views.verification_dashboard, name='verification_dashboard'),
    path('approve-verification/<int:verification_id>/<str:action>/', views.approve_verification, name='approve_verification'),
]
