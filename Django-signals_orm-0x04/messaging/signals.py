from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Signal to send a notification when a new message is sent"""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def save_message_edit_history(sender, instance, **kwargs):
    """Signal to save message edit history when a message is being edited"""
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # If the message does not exist, it's a new message
        # Which means this is not an edit, it's a creation
        return
    
    if old_message.content != instance.content:
        # Content has changed, save the old content to MessageHistory
        MessageHistory.objects.create(
            message=old_message,
            edited_by=old_message.sender,
            old_content=old_message.content
        )
        instance.edited = True  # Mark the message as edited


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Signal to delete all messages, notifications, and message histories
        associated with the user, when the user is deleted
        this logic is not necessary because fk relationships with user have on_delete=models.CASCADE
        if a user is deleted:
            - All their messages sent & received are deleted
            - All notifications sent to them are deleted
            - Notifications sent by them are deleted too, because the messages they sent that triggered those notifications are deleted
            - All message history entries related to their messages are deleted (on message deletion)
    """
    """
    # Delete message history of messages sent by the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    # Delete message history of messages received by the user
    MessageHistory.objects.filter(message__receiver=instance).delete()

    # Delete notifications received by the user
    Notification.objects.filter(user=instance).delete()
    # Delete notifications sent by the user
    Notification.objects.filter(message__sender=instance).delete()

    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    """
    pass