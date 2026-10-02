# social/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Esta función se ejecuta automáticamente cada vez que se guarda un objeto User.
    - Si el usuario es nuevo (created=True), crea su objeto Profile automáticamente.
    - Si el usuario ya existía, guarda los cambios de su perfil.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Si el usuario ya tiene un perfil vinculado, guardamos los cambios
        if hasattr(instance, 'profile'):
            instance.profile.save()