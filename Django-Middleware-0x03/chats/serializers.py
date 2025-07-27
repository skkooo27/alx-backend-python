from rest_framework import serializers
from .models import User, Conversation, Message

# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']


# 2. Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
    sent_at = serializers.DateTimeField(read_only=True)
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'message_body', 'sent_at', 'sender_name']

    def get_sender_name(self, obj):
        return obj.sender.first_name + ' ' + obj.sender.last_name

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


# ✅ 3. Cleaned-Up Conversation Serializer (for creation + listing)
class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value
