from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, MessageHistory

def message_history_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-updated_at')

    data = [
        {
            "old_content": entry.old_content,
            "updated_at": entry.updated_at
        }
        for entry in history
    ]

    return JsonResponse(data, safe=False)

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('login')

def get_conversation(request):
    messages = (
        Message.objects
        .filter(parent_message__isnull=True)
        .select_related('sender')
        .prefetch_related('replies__sender', 'replies__replies')  # preload nested replies
    )
    return render(request, 'chat/conversation.html', {'messages': messages})
