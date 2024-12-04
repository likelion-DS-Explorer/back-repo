from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Profile

@receiver(pre_save, sender=Profile)
def set_club_from_is_manager(sender, instance, **kwargs):
    if instance.is_manager:
        instance.club = instance.is_manager