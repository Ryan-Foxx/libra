from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class CustomUserModelTests(TestCase):

    def test_create_user_with_phone_number_and_email(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="first-test",
            last_name="last-test",
            phone_number="09120000000",
            password="password123",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "first-test")
        self.assertEqual(user.last_name, "last-test")
        self.assertEqual(user.phone_number, "09120000000")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            first_name="admin-first",
            last_name="admin-last",
            phone_number="09123334444",
            password="adminpass",
        )

        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertEqual(admin.first_name, "admin-first")
        self.assertEqual(admin.last_name, "admin-last")
        self.assertEqual(admin.phone_number, "09123334444")
        self.assertTrue(admin.check_password("adminpass"))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_must_be_unique(self):
        User.objects.create_user(
            username="user1", email="unique@example.com", phone_number="09121111111", password="123"
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="user2", email="unique@example.com", phone_number="09122222222", password="123"
            )

    def test_phone_number_must_be_unique(self):
        User.objects.create_user(
            username="user1", email="email1@example.com", phone_number="09121111111", password="123"
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="user2", email="email2@example.com", phone_number="09121111111", password="123"
            )
