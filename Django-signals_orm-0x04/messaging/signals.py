from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:  # Only on update
        try:
            old_instance = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_instance.content != instance.content:
            # Save old version
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content
            )

            instance.edited = True
            instance.edited_at = timezone.now()
            instance.edited_by = instance.sender

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
    Notification.objects.filter(user=instance).delete()
