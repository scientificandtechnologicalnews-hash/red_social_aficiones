# social/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment

class UserRegisterForm(UserCreationForm):
    """
    Formulario de registro de usuario que extiende UserCreationForm
    e incluye el correo electrónico como campo obligatorio.
    """
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['username', 'email']


class UserUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar el nombre de usuario y email.
    """
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar la foto de avatar, biografía e intereses del perfil.
    """
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Cuéntanos un poco sobre ti...'}),
            'interests': forms.TextInput(attrs={'placeholder': 'Ej. Fotografía, Senderismo, Programación'}),
        }

class PostForm(forms.ModelForm):
    """
    Formulario para crear nuevas publicaciones con texto e imagen opcional.
    """
    class Meta:
        model = Post
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': '¿Qué afición o proyecto estás compartiendo hoy?'
            }),
        }


class CommentForm(forms.ModelForm):
    """
    Formulario sencillo para enviar comentarios en un post.
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Escribe un comentario...',
                'style': 'width: 80%; padding: 0.4rem; border-radius: 4px; border: 1px solid #ccc;'
            }),
        }