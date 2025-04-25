from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from hsabackend.models.customer import Customer
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_phone_number
from hsabackend.serializers.customer_serializer import CustomerSerializer

class CustomerModelTest(APITestCase):
    def setUp(self):
        # Create a user for the organization
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create an organization
        self.organization = Organization.objects.create(
            org_name='Test Organization',
            org_email='org@example.com',
            org_city='Test City',
            org_state='CA',
            org_zip='12345',
            org_address='123 Test St',
            org_phone='1234567890',
            org_owner_first_name='Test',
            org_owner_last_name='Owner',
            owning_user=self.user
        )

        # Create a customer
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            email='customer@example.com',
            phone='1234567890',
            notes='Test notes',
            organization=self.organization
        )

    def test_customer_creation(self):
        """Test that a customer can be created with the expected values"""
        # Use CustomerSerializer to serialize the customer
        serializer = CustomerSerializer(self.customer)
        data = serializer.data

        # Check that the serialized data contains the expected values
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'Customer')
        self.assertEqual(data['email'], 'customer@example.com')
        self.assertEqual(data['phone'], '1234567890')
        self.assertEqual(data['notes'], 'Test notes')
        self.assertEqual(data['organization']['id'], self.organization.id)

    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Customer: {self.customer.pk}>"
        self.assertEqual(str(self.customer), expected_str)

    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        # Use CustomerSerializer to serialize the customer
        serializer = CustomerSerializer(self.customer)
        data = serializer.data

        # Check that the serialized data contains the expected values
        self.assertEqual(data['id'], self.customer.pk)
        self.assertEqual(data['first_name'], self.customer.first_name)
        self.assertEqual(data['last_name'], self.customer.last_name)
        self.assertEqual(data['email'], self.customer.email)
        self.assertEqual(data['phone'], self.customer.phone)
        self.assertEqual(data['notes'], self.customer.notes)

        # Also check the model's json method for comparison
        expected_json = {
            'id': self.customer.pk,
            'first_name': self.customer.first_name,
            'last_name': self.customer.last_name,
            'email': self.customer.email,
            'phone': format_phone_number(self.customer.phone),
            'notes': self.customer.notes,
        }
        self.assertEqual(self.customer.json(), expected_json)

    def test_validators(self):
        """Test that validators are applied to the fields"""
        # Create a customer with invalid values
        with self.assertRaises(Exception):
            Customer.objects.create(
                first_name='',  # Empty name should fail
                last_name='Customer',
                email='customer@example.com',
                phone='1234567890',
                notes='Test notes',
                organization=self.organization
            )

        with self.assertRaises(Exception):
            Customer.objects.create(
                first_name='Test',
                last_name='',  # Empty last name should fail
                email='customer@example.com',
                phone='1234567890',
                notes='Test notes',
                organization=self.organization
            )

        with self.assertRaises(Exception):
            Customer.objects.create(
                first_name='Test',
                last_name='Customer',
                email='customer@example.com',
                phone='123456789',  # Invalid phone (too short) should fail
                notes='Test notes',
                organization=self.organization
            )

    def test_optional_fields(self):
        """Test that optional fields can be null or blank"""
        # Create a customer without notes
        customer1 = Customer.objects.create(
            first_name='Test2',
            last_name='Customer2',
            email='customer2@example.com',
            phone='9876543210',
            notes=None,  # Notes can be null
            organization=self.organization
        )

        # Use CustomerSerializer to serialize the customer
        serializer1 = CustomerSerializer(customer1)
        data1 = serializer1.data

        # Check that the serialized data has null notes
        self.assertIsNone(data1['notes'])

        # Create a customer with blank notes
        customer2 = Customer.objects.create(
            first_name='Test3',
            last_name='Customer3',
            email='customer3@example.com',
            phone='5678901234',
            notes='',  # Notes can be blank
            organization=self.organization
        )

        # Use CustomerSerializer to serialize the customer
        serializer2 = CustomerSerializer(customer2)
        data2 = serializer2.data

        # Check that the serialized data has empty notes
        self.assertEqual(data2['notes'], '')
