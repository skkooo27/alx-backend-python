from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For Conversations: check if the user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        # For Messages: check if the user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
