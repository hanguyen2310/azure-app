from django.urls import path

from . import views

app_name = 'ebay'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
]