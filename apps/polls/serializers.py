"""Serializers for the polling API: poll creation, publishing, and voting logic."""

from rest_framework import serializers
from django.utils import timezone
from .models import Poll, Choice, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for poll choices (read-only)."""

    class Meta:
        model = Choice
        fields = ['id', 'text']


class ChoicesField(serializers.CharField):
    """Custom field to input choices as a comma-separated string."""

    def to_internal_value(self, data):
        """Convert comma-separated string to list of choice dictionaries."""
        if isinstance(data, str):
            choices = [text.strip() for text in data.split(',') if text.strip()]
            return [{'text': choice} for choice in choices]
        return data

    def to_representation(self, value):
        """Convert choices to comma-separated string representation."""
        if hasattr(value, 'all'):
            choices = value.all()
        else:
            choices = value
        return ', '.join([choice.text for choice in choices])


class PollSerializer(serializers.ModelSerializer):
    """Serializer for polls with status tracking and simplified choice input."""
    
    creator = serializers.StringRelatedField(read_only=True)
    choices = ChoicesField(
        help_text="Enter choices separated by commas (e.g., 'Option A, Option B, Option C')",
        style={'base_template': 'textarea.html'}
    )
    choice_list = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = [
            'id', 'question', 'creator',
            'start_time', 'end_time',
            'is_draft', 'published_at', 'created_at',
            'choices', 'choice_list',
            'status', 'is_active'
        ]
        read_only_fields = [
            'creator', 'published_at', 'created_at', 'status', 'is_active', 'choice_list'
        ]
        extra_kwargs = {
            'start_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'end_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'published_at': {'format': '%Y-%m-%d %H:%M:%S'},
            'created_at': {'format': '%Y-%m-%d %H:%M:%S'},
        }

    def get_choice_list(self, obj):
        """Return serialized list of choices."""
        return ChoiceSerializer(obj.choices.all(), many=True).data

    def get_status(self, obj):
        """Return current poll status."""
        return obj.status()

    def get_is_active(self, obj):
        """Return whether poll is currently active for voting."""
        return obj.is_active()

    def validate(self, data):
        """Validate poll data including choices and time constraints."""
        choices = data.get('choices', [])
        if len(choices) < 2:
            raise serializers.ValidationError("At least two choices are required.")

        start = data.get('start_time')
        end = data.get('end_time')

        if start and end and start >= end:
            raise serializers.ValidationError("End time must be after start time.")

        return data

    def create(self, validated_data):
        """Create poll with choices and handle draft/publish logic."""
        choices_data = validated_data.pop('choices')
        is_draft = validated_data.get('is_draft', False)

        now = timezone.now()

        if not is_draft:
            validated_data['start_time'] = now
            if not validated_data.get('end_time'):
                validated_data['end_time'] = now + timezone.timedelta(minutes=5)

        validated_data['is_draft'] = True
        poll = Poll.objects.create(**validated_data)

        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)

        if not is_draft:
            poll.publish()

        return poll


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for submitting a vote."""
    
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'poll', 'choice', 'voted_at']
        read_only_fields = ['user', 'voted_at']
        extra_kwargs = {
            'voted_at': {'format': '%Y-%m-%d %H:%M:%S'},
        }

    def validate(self, data):
        """Validate vote submission including poll status and timing constraints."""
        poll = data['poll']
        user = self.context['request'].user
        now = timezone.now().replace(microsecond=0)

        if poll.is_draft:
            raise serializers.ValidationError({
                "non_field_errors": ["This poll has not been published."]
            })

        if not poll.start_time or not poll.end_time:
            raise serializers.ValidationError({
                "non_field_errors": ["This poll has invalid start or end time."]
            })

        if now < poll.start_time:
            raise serializers.ValidationError({
                "non_field_errors": ["This poll is not yet open for voting."]
            })

        if now >= poll.end_time:
            raise serializers.ValidationError({
                "non_field_errors": ["This poll has ended."]
            })

        if Vote.objects.filter(poll=poll, user=user).exists():
            raise serializers.ValidationError({
                "non_field_errors": ["You have already voted on this poll."]
            })

        return data