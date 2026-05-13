from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile yaratildi: {instance.username}")
    else:
        instance.profile.save()
        print(f"Profile update boldi: {instance.username}")


@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete()
        print(f"Profile o'chirildi: {instance.username}")
    except Profile.DoesNotExist:
        pass
    