from django.test import TestCase
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.material import Material

class JobTemplateModelTest(TestCase):
    """Test cases for the JobTemplate model"""
    
    def setUp(self):
        """Set up test data"""
        self.organization = Organization.objects.create(
            name="Test Organization",
            address="123 Test St",
            city="Test City",
            state="TS",
            zip_code="12345",
            phone="1234567890",
            email="test@example.com"
        )
        
        self.service = Service.objects.create(
            name="Test Service",
            description="Test Service Description",
            fee=100.00,
            organization=self.organization
        )
        
        self.material = Material.objects.create(
            name="Test Material",
            description="Test Material Description",
            unit_price=10.00,
            organization=self.organization
        )
        
        self.job_template = JobTemplate.objects.create(
            name="Test Job Template",
            description="Test Job Template Description",
            organization=self.organization
        )
        
        # Add services and materials to the job template
        self.job_template.services.add(self.service)
        self.job_template.materials.add(self.material)
    
    def test_job_template_creation(self):
        """Test that a job template can be created"""
        self.assertEqual(self.job_template.name, "Test Job Template")
        self.assertEqual(self.job_template.description, "Test Job Template Description")
        self.assertEqual(self.job_template.organization, self.organization)
        self.assertEqual(list(self.job_template.services.all()), [self.service])
        self.assertEqual(list(self.job_template.materials.all()), [self.material])
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Job, organization: {self.organization}, description: {self.job_template.description}>"
        self.assertEqual(str(self.job_template), expected_str)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            'id': self.job_template.pk,
            'description': "Test Job Template Description",
        }
        self.assertEqual(self.job_template.json(), expected_json)
    
    def test_json_simplify_method(self):
        """Test the json_simplify method"""
        expected_json = {
            'id': self.job_template.pk,
            'description': "Test Job Template Description",
        }
        self.assertEqual(self.job_template.json_simplify(), expected_json)
    
    def test_json_simplify_method_with_long_description(self):
        """Test the json_simplify method with a long description"""
        # Create a job template with a long description
        long_description = "A" * 100  # 100 characters
        job_template = JobTemplate.objects.create(
            name="Long Description Template",
            description=long_description,
            organization=self.organization
        )
        
        expected_json = {
            'id': job_template.pk,
            'description': long_description[:50] + "...",
        }
        self.assertEqual(job_template.json_simplify(), expected_json)
    
    def test_name_required(self):
        """Test that name is required"""
        # Try to create a job template without a name
        job_template = JobTemplate(
            description="Test Description",
            organization=self.organization
        )
        # Django's model validation should catch this
        with self.assertRaises(Exception):
            job_template.full_clean()
    
    def test_description_optional(self):
        """Test that description is optional"""
        # Create a job template without a description
        job_template = JobTemplate.objects.create(
            name="No Description Template",
            description="",
            organization=self.organization
        )
        self.assertEqual(job_template.description, "")