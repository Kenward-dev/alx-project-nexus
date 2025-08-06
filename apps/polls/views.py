"""Views for the polling API."""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer


class PollViewSet(viewsets.ModelViewSet):
    """ViewSet for creating, retrieving, updating, publishing, and viewing poll results."""
    
    queryset = Poll.objects.prefetch_related('choices').select_related('creator')
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Set the poll creator to the current user."""
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Return appropriate permissions based on action."""
        if self.action in ['update', 'partial_update', 'destroy', 'publish', 'results']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """Return optimized queryset with prefetched relations."""
        return Poll.objects.prefetch_related('choices').select_related('creator')

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        """Publish a draft poll."""
        poll = self.get_object()
        if not poll.is_draft:
            return Response({"detail": "Poll is already published."}, status=status.HTTP_400_BAD_REQUEST)

        if poll.choices.count() < 2:
            return Response({"detail": "Poll must have at least two choices before publishing."}, status=status.HTTP_400_BAD_REQUEST)

        if not poll.start_time or not poll.end_time:
            return Response({"detail": "Start and end time must be set before publishing."}, status=status.HTTP_400_BAD_REQUEST)

        if poll.start_time >= poll.end_time:
            return Response({"detail": "Start time must be before end time."}, status=status.HTTP_400_BAD_REQUEST)

        poll.publish()
        return Response({"detail": "Poll published successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        """Return poll results after it ends. Only accessible to poll creator or admin."""
        poll = self.get_object()

        if timezone.now() <= poll.end_time:
            raise PermissionDenied("Poll results are available after the poll ends.")

        if request.user != poll.creator and not request.user.is_staff:
            raise PermissionDenied("You are not authorized to view results for this poll.")

        total_votes = poll.vote_set.count()
        result = []

        for choice in poll.choices.all():
            vote_count = choice.vote_set.count()
            percent = (vote_count / total_votes * 100) if total_votes else 0
            result.append({
                'choice': choice.text,
                'votes': vote_count,
                'percentage': round(percent, 2)
            })

        return Response({
            'poll': poll.question,
            'status': poll.status(),
            'total_votes': total_votes,
            'results': result
        })


class VoteViewSet(viewsets.ModelViewSet):
    """ViewSet for casting votes. Each user can vote once per poll."""
    
    queryset = Vote.objects.select_related('poll', 'choice', 'user')
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Set the voter to the current user."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return votes filtered by current user."""
        return self.queryset.filter(user=self.request.user)