from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass')
        self.recipient = User.objects.create_user(username='bob', password='pass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, recipient=self.recipient, content='Hello Bob')
        notification = Notification.objects.filter(to_user=self.recipient, message=msg).first()
        self.assertIsNotNone(notification)

    def test_no_duplicate_notification_on_update(self):
        message = Message.objects.create(sender=self.sender, recipient=self.recipient, content="Hello!")
        message.content = "Updated content"
        message.save()
        self.assertEqual(Notification.objects.count(), 1)
