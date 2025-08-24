from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'user_id', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)
