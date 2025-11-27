from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MessageViewSet, NotificationViewSet, UserViewSet, MessageHistoryViewSet
from .views import delete_user, threads

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', UserViewSet)
router.register(r'message-history', MessageHistoryViewSet)

urlpatterns = router.urls + [
    path('delete-user/', delete_user),
    path('threads/', threads, name='threads'),
]