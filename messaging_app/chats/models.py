from django.db import models

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Use UUID as primary key
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Additional fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('user', 'User'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    
    # Override username field to email if desired
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # still required by AbstractUser
    
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conversation {self.conversation_id}"
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"
