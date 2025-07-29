from django.shortcuts import get_object_or_404, redirect
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


@login_required
def get_conversation(request):
    # Top-level unread messages
    messages = Message.unread_objects.for_user(request.user).filter(
        parent_message__isnull=True
    ).select_related('sender').prefetch_related('replies__sender').only(
        'id', 'content', 'sender', 'timestamp', 'parent_message'
    )

    # Recursive function to fetch threaded replies
    def get_threaded_replies(message):
        replies = Message.objects.filter(
            parent_message=message,
            receiver=request.user,
            read=False
        ).select_related('sender').prefetch_related('replies__sender').only(
            'id', 'content', 'sender', 'timestamp', 'parent_message'
        )

        return [
            {
                'id': reply.id,
                'sender': reply.sender.username,
                'content': reply.content,
                'replies': get_threaded_replies(reply)
            } for reply in replies
        ]

    data = [
        {
            'id': message.id,
            'sender': message.sender.username,
            'content': message.content,
            'replies': get_threaded_replies(message)
        } for message in messages
    ]

    return JsonResponse({'messages': data})

@require_GET
def unread_messages_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    unread_messages = Message.unread.unread_for_user(request.user)

    messages_data = []
    for message in unread_messages:
        messages_data.append({
            'id': message.id,
            'sender': message.sender.username,
            'subject': message.subject,
            'body': message.body,
            'timestamp': message.timestamp,
        })

    return JsonResponse({'unread_messages': messages_data})


@cache_page(60)  # Cache this view for 60 seconds
def conversation_messages_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('-timestamp')
    data = [
        {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
        }
        for message in messages
    ]
    return JsonResponse({"messages": data})