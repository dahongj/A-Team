from django.test import TestCase
from .models import User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        # This method is called before each test.
        User.objects.create(email="test@example.com", last_name="Doe", first_name="John", username="johndoe", password="password123")

    def test_user_creation(self):
        # Test to check if user is created successfully.
        john = User.objects.get(email="test@example.com")
        self.assertEqual(john.first_name, "John")
