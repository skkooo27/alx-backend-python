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


# 3. Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.conversation_messages.all()
        return MessageSerializer(messages, many=True).data
