from django.db import models
from user_control.models import *
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="message_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="message_receiver", on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message between {self.sender.first_name} and {self.receiver.first_name}"

    class Meta:
        ordering = ("-created_at",)