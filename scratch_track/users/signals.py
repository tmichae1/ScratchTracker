from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from . idgenerator import generate_id
from.models import Profile


@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        full_name = "{0} {1}".format(instance.first_name.strip().title(), instance.last_name.strip().title())
        Profile.objects.create(profile_id=generate_id(), full_name=full_name, user=instance)
