from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.material import Material

class JobTemplateModelTest(TestCase):
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
        
        # Create services
        self.service1 = Service.objects.create(
            service_name='Test Service 1',
            service_description='Test Service Description 1',
            organization=self.organization,
            default_fee=Decimal('100.00')
        )
        
        self.service2 = Service.objects.create(
            service_name='Test Service 2',
            service_description='Test Service Description 2',
            organization=self.organization,
            default_fee=Decimal('150.00')
        )
        
        # Create materials
        self.material1 = Material.objects.create(
            material_name='Test Material 1',
            material_description='Test Material Description 1',
            organization=self.organization,
            default_cost=Decimal('50.00')
        )
        
        self.material2 = Material.objects.create(
            material_name='Test Material 2',
            material_description='Test Material Description 2',
            organization=self.organization,
            default_cost=Decimal('75.00')
        )
        
        # Create a job template
        self.job_template = JobTemplate.objects.create(
            name='Test Job Template',
            description='Test Job Template Description',
            organization=self.organization
        )
        
        # Add services and materials to the job template
        self.job_template.services.add(self.service1, self.service2)
        self.job_template.materials.add(self.material1, self.material2)
    
    def test_job_template_creation(self):
        """Test that a job template can be created with the expected values"""
        self.assertEqual(self.job_template.name, 'Test Job Template')
        self.assertEqual(self.job_template.description, 'Test Job Template Description')
        self.assertEqual(self.job_template.organization, self.organization)
        
        # Check that services and materials were added
        self.assertEqual(self.job_template.services.count(), 2)
        self.assertIn(self.service1, self.job_template.services.all())
        self.assertIn(self.service2, self.job_template.services.all())
        
        self.assertEqual(self.job_template.materials.count(), 2)
        self.assertIn(self.material1, self.job_template.materials.all())
        self.assertIn(self.material2, self.job_template.materials.all())
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Job, organization: {self.organization}, description: {self.job_template.description}>"
        self.assertEqual(str(self.job_template), expected_str)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            'id': self.job_template.pk,
            'description': self.job_template.description,
        }
        self.assertEqual(self.job_template.json(), expected_json)
    
    def test_json_simplify_method(self):
        """Test the json_simplify method returns the expected dictionary"""
        expected_json = {
            'id': self.job_template.pk,
            'description': self.job_template.description[:50] + ("..." if len(self.job_template.description) > 50 else ""),
        }
        self.assertEqual(self.job_template.json_simplify(), expected_json)
    
    def test_json_simplify_method_with_long_description(self):
        """Test the json_simplify method truncates long descriptions"""
        # Create a job template with a long description
        long_description = "A" * 100  # 100 'A' characters
        job_template = JobTemplate.objects.create(
            name='Test Job Template with Long Description',
            description=long_description,
            organization=self.organization
        )
        
        expected_json = {
            'id': job_template.pk,
            'description': long_description[:50] + "...",
        }
        self.assertEqual(job_template.json_simplify(), expected_json)
    
    def test_optional_fields(self):
        """Test that optional fields can be blank"""
        # Create a job template without a description
        job_template = JobTemplate.objects.create(
            name='Test Job Template 2',
            description='',  # Empty description should be allowed
            organization=self.organization
        )
        
        self.assertEqual(job_template.description, '')
        
        # Create a job template without services and materials
        job_template = JobTemplate.objects.create(
            name='Test Job Template 3',
            description='Test Job Template Description 3',
            organization=self.organization
        )
        
        self.assertEqual(job_template.services.count(), 0)
        self.assertEqual(job_template.materials.count(), 0)
    
    def test_multiple_job_templates(self):
        """Test that multiple job templates can be created for the same organization"""
        # Create additional job templates
        job_template2 = JobTemplate.objects.create(
            name='Test Job Template 2',
            description='Test Job Template Description 2',
            organization=self.organization
        )
        
        job_template3 = JobTemplate.objects.create(
            name='Test Job Template 3',
            description='Test Job Template Description 3',
            organization=self.organization
        )
        
        # Verify that all job templates are associated with the same organization
        job_templates = JobTemplate.objects.filter(organization=self.organization)
        self.assertEqual(job_templates.count(), 3)
        self.assertIn(self.job_template, job_templates)
        self.assertIn(job_template2, job_templates)
        self.assertIn(job_template3, job_templates)