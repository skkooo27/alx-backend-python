# Generated by Django 5.2.4 on 2025-07-29 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_rename_recipient_message_receiver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parent_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='messaging.message'),
        ),
    ]
