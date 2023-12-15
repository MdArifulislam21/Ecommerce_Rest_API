from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()

""" 
When a user will create. A Profile of that user will also create automatically throught 
this signals.
"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

""" 
When a user will Update. Profile of that user will also update automatically throught 
this signals.
"""
@receiver(post_save, sender=User)
def save_profile(sender, instance,  created, **kwargs):
    if not created:
        instance.profile.save()
