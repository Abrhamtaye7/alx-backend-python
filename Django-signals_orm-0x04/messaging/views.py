from rest_framework import viewsets
from .models import Message, Notification, MessageHistory
from .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer, ThreadMessageSerializer, UnreadMessageSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @method_decorator(cache_page(60))  # cache for 1 minute
    def list(self, request, *args, **kwargs):
        print("querying the db *******************")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """ The sender of a reply is the logged-in user sending it
            The receiver of a reply is the other participant in the parent message

            Example: Conversation between A and B:
                - Message 1: A sends to B
                    - If A replies to this message -> it goes to B
                    - If B replies to this message -> it goes to A
                - Message 2: B sends to A
                    - If B replies to this message -> it goes to A
                    - If A replies to this message -> it goes to B
            
            Maintains a conversation between two users
        """
        parent_message = serializer.validated_data.get('parent_message')
        if parent_message:  # if it's a reply
            # User replies to their own message in a conversation (A replies to 1)
            if self.request.user == parent_message.sender:
                serializer.save(sender=self.request.user, receiver=parent_message.receiver)
            # User replies to the other user's message (B replies to 1)
            elif self.request.user == parent_message.receiver:
                serializer.save(sender=self.request.user, receiver=parent_message.sender)
        else:
            # normal message
            serializer.save(sender=self.request.user)
    
    @action(detail=False, permission_classes=[IsAuthenticated])
    def unread(self, request):
        """route: messages/unread/"""
        queryset = Message.unread.unread_for_user(request.user)\
                        .only('id', 'sender', 'content', 'timestamp')
        serializer = UnreadMessageSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threads(request):
    """
    Returns all top-level messages (messages with no parent) and their full reply trees.
    Replies are prefetched to avoid extra database queries.
    """
    sender=request.user
    # Prefetch replies with sender and receiver
    replies_prefetch = Prefetch(
        'replies',
        queryset=Message.objects.select_related('sender', 'receiver').all()
    )

    top_messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            replies_prefetch,
            Prefetch('replies__replies', queryset=Message.objects.select_related('sender', 'receiver').all())
        )

    serializer = ThreadMessageSerializer(top_messages, many=True)
    return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """A view that deletes the currently logged-in user"""
    user = request.user
    user.delete()
    return Response({'status': 'User deleted'})


class MessageHistoryViewSet(viewsets.ModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer