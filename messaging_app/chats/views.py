from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework import status as drf_status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from .filters import MessageFilter
from .pagination import MessagePagination


class ForbiddenException(APIException):
    status_code = drf_status.HTTP_403_FORBIDDEN
    default_detail = "You are not allowed to perform this action."
    default_code = "forbidden"


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()  # ✅ Required by DRF
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participants = serializer.validated_data.get('participants')
        if request.user not in participants:
            raise ForbiddenException("You must be a participant in the conversation.")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__username', 'content']
    ordering_fields = ['timestamp']


    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise ForbiddenException(f"You are not a participant of conversation {conversation.id}.")
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            raise ForbiddenException(f"You are not a participant of conversation {message.conversation.id}.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            raise ForbiddenException(f"You are not a participant of conversation {message.conversation.id}.")
        return super().destroy(request, *args, **kwargs)
