# social/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm
from .models import Profile, Post

def register(request):
    """
    Vista de registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada con éxito para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'social/register.html', {'form': form})


@login_required
def profile_edit(request):
    """
    Vista protegida para editar los datos del usuario y su foto de perfil.
    Recibe request.FILES para procesar la subida del avatar de forma segura.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Importante: request.FILES procesa la subida de la imagen del avatar
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado correctamente!')
            return redirect('profile_detail', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'social/profile_edit.html', context)


def profile_detail(request, username):
    """
    Muestra el perfil público de un usuario especificado por su nombre de usuario.
    """
    user_profile = get_object_or_404(User, username=username)
    return render(request, 'social/profile_detail.html', {'user_profile': user_profile})

@login_required
def my_profile_redirect(request):
    """
    Redirige automáticamente al usuario autenticado a su propia página de perfil.
    """
    return redirect('profile_detail', username=request.user.username)

@login_required
def feed(request):
    """
    Muestra el muro principal con las publicaciones y procesa la creación de nuevos posts.
    """
    if request.method == 'POST':
        # Pasamos request.FILES para procesar la imagen adjunta
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # Asignamos el autor logueado
            post.save()
            messages.success(request, '¡Tu publicación ha sido compartida!')
            return redirect('feed')
    else:
        form = PostForm()

    # De momento traemos todas las publicaciones recientes
    posts = Post.objects.all()

    return render(request, 'social/feed.html', {'form': form, 'posts': posts})
# Create your views here.
