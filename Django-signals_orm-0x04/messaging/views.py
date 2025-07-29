from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message, MessageHistory

def message_history_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-edited_at')

    data = [
        {
            "previous_content": entry.previous_content,
            "edited_at": entry.edited_at,
            "edited_by": entry.edited_by.username if entry.edited_by else None
        }
        for entry in history
    ]

    return JsonResponse(data, safe=False)
