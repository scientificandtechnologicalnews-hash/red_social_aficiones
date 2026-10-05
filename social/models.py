from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    """
    Extiende la información del usuario sin modificar el modelo User de Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografía")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name="Foto de perfil")
    interests = models.CharField(max_length=200, blank=True, verbose_name="Intereses/Aficiones")

    def __str__(self):
        return f'Perfil de {self.user.username}'

class Post(models.Model):
    """
    Publicaciones del usuario con soporte para texto e imagen.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(verbose_name="Contenido")
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Imagen del post")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post de {self.author.username} ({self.created_at.date()})'

class Follow(models.Model):
    """
    Relación 'Seguir' y 'Dejar de seguir'. 
    """
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user_from', 'user_to') # Evita seguir dos veces a la misma persona

    def __str__(self):
        return f'{self.user_from} sigue a {self.user_to}'


class Comment(models.Model):
    """
    Modelo para almacenar los comentarios realizados por los usuarios en las publicaciones.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Publicación")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name="Autor")
    text = models.TextField(max_length=300, verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        ordering = ['created_at'] # Los comentarios se muestran del más antiguo al más reciente

    def __str__(self):
        return f'Comentario de {self.author.username} en post #{self.post.id}'


class Like(models.Model):
    """
    Modelo para gestionar los 'Me gusta' de los usuarios en cada publicación.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name="Publicación")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes', verbose_name="Usuario")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garantiza que un usuario solo pueda dar 'Me gusta' una vez por publicación
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.username} le gusta la publicación #{self.post.id}'
# Create your models here.
