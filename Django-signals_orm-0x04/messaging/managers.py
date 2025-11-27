from django.db import models


class UnreadMessagesManager(models.Manager):
    """A custom manager that filter unread received messages for a specific user"""

    def unread_for_user(self, user):
        return self.filter(receiver=user, is_read=False).order_by('-timestamp')