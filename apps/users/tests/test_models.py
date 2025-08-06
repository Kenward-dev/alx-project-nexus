"""
Tests for custom User model.
"""

import uuid
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    """Test cases for the custom User model."""

    def test_create_user_with_email(self):
        """Test creating a user with email."""
        email = "ken@pollapi.com"
        password = "testpass123"
        user = User.objects.create_user(
            username="ken",
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(isinstance(user.id, uuid.UUID))

    def test_user_string_representation(self):
        """Test the string representation of user."""
        email = "ken@pollapi.com"
        user = User.objects.create_user(
            username="ken",
            email=email,
            password="testpass123"
        )
        
        self.assertEqual(str(user), email)

    def test_email_unique_constraint(self):
        """Test that email must be unique."""
        email = "ken@pollapi.com"
        User.objects.create_user(
            username="ken1",
            email=email,
            password="testpass123"
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="ken2",
                email=email,
                password="testpass123"
            )

    def test_uuid_primary_key(self):
        """Test that user ID is a UUID."""
        user = User.objects.create_user(
            username="ken",
            email="ken@pollapi.com",
            password="testpass123"
        )
        
        self.assertIsInstance(user.id, uuid.UUID)
        self.assertIsNotNone(user.id)