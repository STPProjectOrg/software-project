from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from user_app.models import UserProfileInfo
from django.conf import settings
import os

@receiver(pre_save, sender=UserProfileInfo)
def delete_old_profile_pic(sender, instance, **kwargs):
    """
    This signal receiver function is triggered before saving a UserProfileInfo instance. 
    It is responsible for deleting the old profile picture file from the filesystem when 
    the user updates their profile picture.

    Keyword arguments:
        pre_save: Signal will be triggered before saving an instance of the UserProfileInfo model
        sender: Specifies the "UserProfileInfo"-model class that sends the signal
        instance: Instance of the UserProfileInfo model which represents the data that is being updated
    """
    if instance.pk:
        old_instance = UserProfileInfo.objects.get(pk=instance.pk)
        if old_instance.profile_pic:
            old_path = old_instance.profile_pic.path
            if os.path.exists(old_path):
                os.remove(old_path)

                
@receiver(post_delete, sender=UserProfileInfo)
def delete_profile_pic_file(sender, instance, **kwargs):
    """
    This signal receiver function is triggered after deleting a UserProfileInfo instance. 
    It is responsible for deleting the associated profile picture file from the filesystem 
    when the UserProfileInfo instance is deleted.

    Receiver arguments:
        post_delete: Signal will be triggered after deleting an instance of the UserProfileInfo model
        sender: Specifies the "UserProfileInfo"-model class that sends the signal
        instance: Instance of the UserProfileInfo model which represents the data that is being deleted
    """
    if instance.profile_pic:
        file_path = instance.profile_pic.path
        if os.path.exists(file_path):
            os.remove(file_path)