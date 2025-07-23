from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']

    def get_queryset(self):
        # Only show conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user is included in the participants
        participants = serializer.validated_data.get('participants')
        if request.user not in participants:
            raise PermissionDenied("You must be a participant in the conversation.")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']

    def get_queryset(self):
        # Only show messages in conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")

        # Only participants can send messages
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")

        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        return super().destroy(request, *args, **kwargs)
