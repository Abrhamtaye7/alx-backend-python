from rest_framework import serializers
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'is_read', 'parent_message', 'replies', 'history']
    
    def get_history(self, obj):
        # Retrieve the edit history of the current message
        history_qs = obj.history.all().order_by('-edited_at')
        return MessageHistorySerializer(history_qs, many=True).data

    def get_replies(self, obj):
        # Retrieve the replies to the current message
        replies_qs = obj.replies.all().order_by('-timestamp')
        return MessageSerializer(replies_qs, many=True).data


class ThreadMessageSerializer(serializers.ModelSerializer):
    """Same as MessageSerializer, but without edit history, used for threads"""
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'parent_message', 'replies']

    def get_replies(self, obj):
        replies_qs = obj.replies.all().order_by('-timestamp')
        return ThreadMessageSerializer(replies_qs, many=True).data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = '__all__'


class UnreadMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']