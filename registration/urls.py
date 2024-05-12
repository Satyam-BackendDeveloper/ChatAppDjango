from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', views.Login.as_view(), name='login-django'),
    # path('logout/', views.Logout.as_view(), name='logout-django'),
    # path('signup/', views.Signup.as_view(), name='signup-django'),
    path('signup/', views.signup_func_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]