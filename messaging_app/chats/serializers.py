from rest_framework import serializers
from .models import User, Conversation, Message

# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # computed field

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# -------------------------
# Message Serializer
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=500)  # explicit CharField

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# -------------------------
# Conversation Serializer (Read)
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()  # computed field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'total_messages']

    def get_total_messages(self, obj):
        return obj.messages.count()


# -------------------------
# Conversation Create Serializer (Write)
# -------------------------
class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    title = serializers.CharField(max_length=100, required=False)  # example field
     
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'title']

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation

    def update(self, instance, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        instance.participants.set(participant_ids)
        return super().update(instance, validated_data)