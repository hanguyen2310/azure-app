from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'
urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='index'),
    path('<str:username>', views.user_page, name='user_page'),
]