from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from . import models

User = get_user_model()

@receiver(post_save, sender = User)
def save_profile(sender, instance, created, **kwargs):
    if created  & instance.is_superuser:
        profile = models.Profile.objects.create(
            user = instance,
            gender = models.Profile.MALE,
            address = "test",
            phone = 'test',
        )
