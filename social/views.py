# social/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from .models import Profile, Post, Follow, Comment, Like

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
    Muro principal que filtra y muestra solo publicaciones de usuarios seguidos y las propias.
    """
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '¡Tu publicación ha sido compartida!')
            return redirect('feed')
    else:
        form = PostForm()

    # Obtener los IDs de los usuarios que el usuario actual sigue
    following_ids = Follow.objects.filter(user_from=request.user).values_list('user_to_id', flat=True)

    # Filtrar publicaciones: usuarios seguidos O publicaciones propias
    posts = Post.objects.filter(
        Q(author_id__in=following_ids) | Q(author=request.user)
    ).distinct()

    comment_form = CommentForm()

    context = {
        'form': form,
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'social/feed.html', context)

@login_required
def follow_toggle(request, username):
    """
    Vista para procesar la acción de seguir o dejar de seguir a un usuario.
    """
    target_user = get_object_or_404(User, username=username)

    # Evitamos que un usuario pueda seguirse a sí mismo
    if target_user == request.user:
        messages.warning(request, "No puedes seguirte a ti mismo.")
        return redirect('profile_detail', username=username)

    # Buscamos si ya existe la relación de seguimiento
    follow_relation = Follow.objects.filter(user_from=request.user, user_to=target_user)

    if follow_relation.exists():
        follow_relation.delete()
        messages.info(request, f"Has dejado de seguir a {target_user.username}.")
    else:
        Follow.objects.create(user_from=request.user, user_to=target_user)
        messages.success(request, f"Ahora sigues a {target_user.username}.")

    return redirect('profile_detail', username=username)

@login_required
def profile_detail(request, username):
    """
    Muestra el perfil público, contadores de seguidores/seguidos y las publicaciones propias del usuario.
    """
    user_profile = get_object_or_404(User, username=username)

    # Verificamos si el usuario logueado sigue a este perfil
    is_following = Follow.objects.filter(user_from=request.user, user_to=user_profile).exists()

    # Contadores de relaciones
    followers_count = user_profile.rel_to_set.count() # Cuántos lo siguen
    following_count = user_profile.rel_from_set.count() # A cuántos sigue

    # Publicaciones creadas por este usuario
    user_posts = user_profile.posts.all()

    context = {
        'user_profile': user_profile,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'user_posts': user_posts,
    }
    return render(request, 'social/profile_detail.html', context)


@login_required
def add_comment(request, post_id):
    """
    Procesa el envío de un nuevo comentario hacia una publicación específica.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comentario publicado.')
    return redirect('feed')


@login_required
def like_toggle(request, post_id):
    """
    Alterna la reacción 'Me gusta' de un usuario sobre una publicación.
    """
    post = get_object_or_404(Post, id=post_id)
    like_qs = Like.objects.filter(post=post, user=request.user)

    if like_qs.exists():
        like_qs.delete() # Si ya tenía 'Me gusta', lo elimina
    else:
        Like.objects.create(post=post, user=request.user) # Si no, lo crea

    return redirect('feed')
# Create your views here.
