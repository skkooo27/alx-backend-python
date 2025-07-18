from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats import views

router = NestedDefaultRouter()

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
