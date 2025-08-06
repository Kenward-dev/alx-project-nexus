"""
Models for the polling system.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    """
    A poll containing a question and multiple choices.
    Supports drafts, scheduling, and voting window.
    """
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="polls"
    )
    question = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question

    def publish(self):
        """
        Publish the poll by marking it as not draft and setting the published timestamp.
        """
        if self.is_draft:
            self.is_draft = False
            self.published_at = timezone.now()
            self.save()
            return True
        return False

    def is_active(self):
        """
        Return True if the poll is published and the current time is within the voting window.
        """
        now = timezone.now()
        return (
            not self.is_draft and
            self.start_time and self.end_time and
            self.start_time <= now < self.end_time  # strict enforcement
        )

    def status(self):
        """
        Return a string representing the poll's current status.
        """
        now = timezone.now()
        if self.is_draft:
            return "Draft"
        if not self.start_time or not self.end_time:
            return "Invalid"
        if now < self.start_time:
            return "Scheduled"
        elif self.start_time <= now < self.end_time:
            return "Active"
        else:
            return "Ended"


class Choice(models.Model):
    """
    A choice belonging to a poll.
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Vote(models.Model):
    """
    A user's vote on a specific choice of a poll.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll')

    def __str__(self):
        return f"{self.user} voted for {self.choice.text} on poll {self.poll.id}"
