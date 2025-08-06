"""
Custom email classes for user activation and password reset using Djoser.
Adds support for dynamic site name, timestamp, and clean message formatting.
"""

from djoser.email import (
    ActivationEmail as DjoserActivationEmail,
    PasswordResetEmail as DjoserPasswordResetEmail
)
from datetime import datetime
from django.conf import settings


class ActivationEmail(DjoserActivationEmail):
    """
    Custom activation email sent to users after registration.
    """

    def get_context_data(self):
        """
        Returns the context used for rendering the activation email.

        Adds:
        - site_name: From settings or default to 'Polls API'
        - now: Current timestamp
        """
        context = super().get_context_data()
        context.update({
            'site_name': getattr(settings, 'SITE_NAME', 'Polls API'),
            'now': datetime.now(),
        })
        return context

    def get_subject(self):
        """
        Returns the email subject line for activation.
        """
        return "Activate your account"

    def get_body(self):
        """
        Returns the plain text body of the activation email.
        Includes an activation link constructed with UID and token.
        """
        context = self.get_context_data()
        activation_url = f"{settings.FRONTEND_URL}/api/v1/auth/users/activation/{context['uid']}/{context['token']}/"
        return (
            f"Hello {context['user'].get('email')},\n\n"
            f"Thank you for registering with {context['site_name']}.\n"
            f"Please activate your account by clicking the link below:\n\n"
            f"{activation_url}\n\n"
            f"This link will expire shortly.\n"
            f"Sent at {context['now'].strftime('%Y-%m-%d %H:%M:%S')}."
        )


class PasswordResetEmail(DjoserPasswordResetEmail):
    """
    Custom password reset email sent when a user requests a reset.
    """

    def get_context_data(self):
        """
        Returns the context used for rendering the password reset email.

        Adds:
        - site_name: From settings or default to 'Polls API'
        - now: Current timestamp
        """
        context = super().get_context_data()
        context.update({
            'site_name': getattr(settings, 'SITE_NAME', 'Polls API'),
            'now': datetime.now(),
        })
        return context

    def get_subject(self):
        """
        Returns the email subject line for password reset.
        """
        return "Reset your password"

    def get_body(self):
        """
        Returns the plain text body of the password reset email.
        Includes a reset link constructed with UID and token.
        """
        context = self.get_context_data()
        reset_url = f"{settings.FRONTEND_URL}/password/reset/confirm/{context['uid']}/{context['token']}/"
        return (
            f"Hello {context['user'].get('email')},\n\n"
            f"We received a request to reset your password on {context['site_name']}.\n"
            f"You can reset it using the link below:\n\n"
            f"{reset_url}\n\n"
            f"Sent at {context['now'].strftime('%Y-%m-%d %H:%M:%S')}."
        )
