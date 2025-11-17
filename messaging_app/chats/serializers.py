from rest_framework import serializers
from .models import User, Conversation, Message

# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role']


# -------------------------
# Message Serializer
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested user info

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# -------------------------
# Conversation Serializer (Read)
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']


# -------------------------
# Conversation Create Serializer (Write)
# -------------------------
class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation
