from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('add/', views.add, name='add'),
    path('ajax/preview/', views.ajax_preview, name='ajax_preview'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/edit/edit_confirm/', views.edit_confirm, name='edit_confirm'),
    path('tag/<str:tag>', views.tag_view, name='tag'),
    # path('')
]