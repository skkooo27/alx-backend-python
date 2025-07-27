from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Ensure user is authenticated
        if not user or not user.is_authenticated:
            return False

        # PUT, PATCH, DELETE: stricter permission
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'sender'):
                # Only sender can modify their message
                return obj.sender == user
            elif hasattr(obj, 'participants'):
                # Only participants can modify the conversation
                return user in obj.participants.all()
            else:
                return False

        # For all other methods, user must be a participant
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        return False
