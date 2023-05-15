from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from user_app.models import UserProfileInfo
from django.conf import settings
import os

@receiver(pre_save, sender=UserProfileInfo)
def delete_old_profile_pic(sender, instance, **kwargs):
    if instance.pk:
        old_instance = UserProfileInfo.objects.get(pk=instance.pk)
        if old_instance.profile_pic:
            old_path = old_instance.profile_pic.path
            if os.path.exists(old_path):
                os.remove(old_path)

@receiver(post_delete, sender=UserProfileInfo)
def delete_profile_pic_file(sender, instance, **kwargs):
    if instance.profile_pic:
        file_path = instance.profile_pic.path
        if os.path.exists(file_path):
            os.remove(file_path)