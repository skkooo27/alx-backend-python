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
            "updated_at": entry.updated_at,
            "edited_by": entry.edited_by.username if entry.edited_by else None
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

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')
        receiver = get_object_or_404(User, id=receiver_id)
        parent_id = request.POST.get('parent_id')

        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, id=parent_id)

        Message.objects.create(
            content=content,
            sender=request.user,
            receiver=receiver,
            parent_message=parent_message
        )

        return JsonResponse({'message': 'Message sent successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_conversation(request):
    messages = (
        Message.objects
        .filter(parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')
    )

    def get_threaded_replies(message):
        replies = message.replies.all().select_related('sender', 'receiver').prefetch_related('replies')
        return [
            {
                'id': reply.id,
                'content': reply.content,
                'sender': reply.sender.username,
                'receiver': reply.receiver.username,
                'created_at': reply.created_at,
                'replies': get_threaded_replies(reply)  # Recursive call
            }
            for reply in replies
        ]

    data = []
    for message in messages:
        data.append({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'created_at': message.created_at,
            'replies': get_threaded_replies(message)
        })

    return JsonResponse(data, safe=False)
