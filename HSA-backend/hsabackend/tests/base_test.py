from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate

from hsabackend.models.organization import Organization


class BaseTestCase(APITestCase):
    """
    Base test class that sets up a user and organization for all tests.
    This class implements the "before all" functionality by using the setUpTestData class method,
    which is called once for the entire test class rather than for each test method.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.
        This method is called once for the entire test class.
        It creates a user and an organization that can be used by all test methods.
        """
        # Create a test user
        cls.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # Create a test organization
        cls.test_organization = Organization.objects.create(
            org_name='Test Organization',
            org_email='testorg@example.com',
            org_city='Test City',
            org_state='Iowa',  # Using a valid state as per the validator
            org_zip='12345',
            org_address='123 Test St',
            org_phone='1234567890',
            org_owner_first_name='Test',
            org_owner_last_name='Owner',
            owning_user=cls.test_user,
            is_onboarding=False,
            default_labor_rate=100.00
        )

    def force_authenticate_user(self, request):
        """
        Helper method to force authenticate a request with the test user.
        Use this instead of setting is_authenticated directly.
        """
        force_authenticate(request, user=self.test_user)
