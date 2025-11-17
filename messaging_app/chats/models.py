from django.db import models

import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # UUID primary key
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Explicitly declare fields to satisfy checks
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Django default hash length

    # Extra fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    # Override authentication fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
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
