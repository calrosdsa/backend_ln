from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from profiles.models import Profile
User = get_user_model()

@receiver(post_save, sender=User)
def post_save_created_profile(sender, instance, created, **kwargs):
    print('sender', sender,'instance',instance,'created',created)
    if created:
        Profile.objects.create(user=instance,name=instance,bio='No bio yet')    