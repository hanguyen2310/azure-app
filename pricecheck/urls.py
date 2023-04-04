from django.urls import path

from . import views

app_name = 'pricecheck'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
]