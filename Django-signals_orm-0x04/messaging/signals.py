from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory
from django.utils import timezone

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

            # Mark as edited
            instance.edited = True
            instance.edited_at = timezone.now()
            instance.edited_by = instance.sender  
