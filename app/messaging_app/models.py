from django.db import models
from user_app.models import CustomUser

# Create your models here.
class Inbox(models.Model):
    inbox_from_user = models.ForeignKey(CustomUser ,on_delete=models.CASCADE)
    def __str__(self):
        return self.inbox_from_user
    
class InboxParticipants(models.Model):
    inbox_id = models.ForeignKey(Inbox, on_delete=models.CASCADE)
    participant_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.inbox_id

class Message(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="to_user")
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField()