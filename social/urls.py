# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    
    # Rutas para comentarios y reacciones
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_toggle, name='like_toggle'),
]