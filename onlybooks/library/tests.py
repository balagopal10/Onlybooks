from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Book

class RoleBasedAccessTests(TestCase):
    def setUp(self):
        # Create roles
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        user_group, _ = Group.objects.get_or_create(name="User")

        # Create users
        self.admin = User.objects.create_user(username='admin', password='pass')
        self.admin.groups.add(admin_group)

        self.user = User.objects.create_user(username='user', password='pass')
        self.user.groups.add(user_group)

        # Create a book
        self.book = Book.objects.create(title="Django for Beginners", author="William S. Vincent", available_copies=5)

    def test_admin_access(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get('/dashboard/admin/')
        self.assertEqual(response.status_code, 200)

    def test_user_access(self):
        self.client.login(username='user', password='pass')
        response = self.client.get('/dashboard/user/')
        self.assertEqual(response.status_code, 200)