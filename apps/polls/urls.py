"""URL configuration for the polling API."""

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PollViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'vote', VoteViewSet, basename='votes')

urlpatterns = [
    path('', include(router.urls)),
]