# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Muro principal / portada
    path('', views.feed, name='feed'),

    # Rutas de registro y perfil
    path('register/', views.register, name='register'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
]