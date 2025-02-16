from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path('register',views.register,name="register"),
    path('profile',views.profile,name="profile"),
    path('addmoney',views.addmoney,name="addmoney"),
    path('withdraw',views.withdraw,name="withdraw"),
    path('check',views.check,name="check"),
]