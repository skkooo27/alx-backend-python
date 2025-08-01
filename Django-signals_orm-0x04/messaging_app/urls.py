"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from messaging import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/<int:message_id>/history/', views.message_history_view, name='message_history'),
    path('delete-account/', views.delete_user, name='delete_user'),
    path('messages/', views.get_conversation, name='get_conversation'),
    path('messages/unread/', views.unread_messages_view, name='unread_messages'),
    path('conversation/<int:conversation_id>/messages/', conversation_messages_view, name='conversation_messages'),

]
