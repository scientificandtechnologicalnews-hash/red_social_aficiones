# social/admin.py

from django.contrib import admin
from .models import Profile, Post, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Gestión visual de los perfiles de usuario en el admin.
    """
    list_display = ('user', 'interests', 'avatar')
    search_fields = ('user__username', 'interests')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Gestión visual de las publicaciones con texto e imagen.
    """
    list_display = ('author', 'created_at', 'text', 'image')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Gestión de la relación de seguidores entre usuarios.
    """
    list_display = ('user_from', 'user_to', 'created_at')
    search_fields = ('user_from__username', 'user_to__username')

# Register your models here.
