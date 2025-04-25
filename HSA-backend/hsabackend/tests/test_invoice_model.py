from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from hsabackend.models.invoice import Invoice
from hsabackend.models.customer import Customer
from hsabackend.models.discount import Discount
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from hsabackend.utils.string_formatters import format_maybe_null_date
from datetime import date

class InvoiceModelTest(TestCase):
    def setUp(self):
        # Create a user for the organization
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create an organization
        self.organization = Organization.objects.create(
            name='Test Organization',
            address='123 Test St',
            city='Test City',
            state='TS',
            zip_code='12345',
            phone='1234567890',
            email='org@example.com',
            owner=self.user
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
        
        # Create discounts
        self.discount1 = Discount.objects.create(
            discount_name='Test Discount 1',
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
        
        self.discount2 = Discount.objects.create(
            discount_name='Test Discount 2',
            discount_percent=Decimal('5.00'),
            organization=self.organization
        )
        
        # Create an invoice
        self.invoice = Invoice.objects.create(
            date_issued=date(2023, 1, 1),
            date_due=date(2023, 1, 15),
            status='created',
            sales_tax_percent=Decimal('7.50'),
            customer=self.customer,
            payment_link='https://example.com/payment'
        )
        
        # Add discounts to the invoice
        self.invoice.discounts.add(self.discount1, self.discount2)
        
        # Create a job linked to the invoice
        self.job = Job.objects.create(
            job_status='completed',
            description='Test Job',
            organization=self.organization,
            invoice=self.invoice,
            customer=self.customer,
            job_city='Test City',
            job_state='TS',
            job_zip='12345',
            job_address='123 Test St',
            use_hourly_rate=False,
            minutes_worked=0,
            hourly_rate=Decimal('0.00')
        )
        
        # Create a service
        self.service = Service.objects.create(
            name='Test Service',
            description='Test Service Description',
            fee=Decimal('100.00'),
            organization=self.organization
        )
        
        # Create a material
        self.material = Material.objects.create(
            name='Test Material',
            description='Test Material Description',
            unit_price=Decimal('50.00'),
            quantity=2,
            organization=self.organization
        )
        
        # Add service and material to the job
        self.job.services.add(self.service)
        self.job.materials.add(self.material)
    
    def test_invoice_creation(self):
        """Test that an invoice can be created with the expected values"""
        self.assertEqual(self.invoice.date_issued, date(2023, 1, 1))
        self.assertEqual(self.invoice.date_due, date(2023, 1, 15))
        self.assertEqual(self.invoice.status, 'created')
        self.assertEqual(self.invoice.sales_tax_percent, Decimal('7.50'))
        self.assertEqual(self.invoice.customer, self.customer)
        self.assertEqual(self.invoice.payment_link, 'https://example.com/payment')
        
        # Check that discounts were added
        self.assertEqual(self.invoice.discounts.count(), 2)
        self.assertIn(self.discount1, self.invoice.discounts.all())
        self.assertIn(self.discount2, self.invoice.discounts.all())
    
    def test_subtotal_property(self):
        """Test the subtotal property returns the correct sum of job subtotals"""
        # The job has one service with fee 100.00 and one material with unit_price 50.00 and quantity 2
        # So the job subtotal should be 100.00 + (50.00 * 2) = 200.00
        self.assertEqual(self.job.subtotal, Decimal('200.00'))
        
        # The invoice subtotal should be the sum of all job subtotals
        self.assertEqual(self.invoice.subtotal, Decimal('200.00'))
    
    def test_discount_aggregate_percentage_property(self):
        """Test the discount_aggregate_percentage property returns the correct sum of discount percentages"""
        # The invoice has two discounts with percentages 10.00 and 5.00
        # So the aggregate percentage should be 10.00 + 5.00 = 15.00
        self.assertEqual(self.invoice.discount_aggregate_percentage, Decimal('15.00'))
    
    def test_discounted_subtotal_property(self):
        """Test the discounted_subtotal property returns the correct amount"""
        # The subtotal is 200.00 and the discount percentage is 15.00%
        # So the discounted amount should be 200.00 * 15.00 / 100 = 30.00
        self.assertEqual(self.invoice.discounted_subtotal, Decimal('30.00'))
    
    def test_subtotal_after_discount_property(self):
        """Test the subtotal_after_discount property returns the correct amount"""
        # The subtotal is 200.00 and the discounted amount is 30.00
        # So the subtotal after discount should be 200.00 - 30.00 = 170.00
        self.assertEqual(self.invoice.subtotal_after_discount, Decimal('170.00'))
    
    def test_taxable_amount_property(self):
        """Test the taxable_amount property returns the correct amount"""
        # The subtotal after discount is 170.00 and the sales tax percent is 7.50%
        # So the taxable amount should be 170.00 * 7.50 / 100 = 12.75
        self.assertEqual(self.invoice.taxable_amount, Decimal('12.75'))
    
    def test_total_property(self):
        """Test the total property returns the correct amount"""
        # The subtotal after discount is 170.00 and the taxable amount is 12.75
        # So the total should be 170.00 + 12.75 = 182.75
        self.assertEqual(self.invoice.total, Decimal('182.75'))
    
    def test_str_method(self):
        """Test the __str__ method returns the expected string representation"""
        expected_str = f"<Invoice, customer: {self.customer}>"
        self.assertEqual(str(self.invoice), expected_str)
    
    def test_json_for_view_invoice_method(self):
        """Test the json_for_view_invoice method returns the expected dictionary"""
        expected_json = {
            "id": self.invoice.pk,
            "status": self.invoice.status,
            "dueDate": self.invoice.date_due,
            "issuanceDate": self.invoice.date_issued,
            "customer": f"{self.customer.first_name}, {self.customer.last_name}"
        }
        self.assertEqual(self.invoice.json_for_view_invoice(), expected_json)
    
    def test_json_method(self):
        """Test the json method returns the expected dictionary"""
        expected_json = {
            "id": self.invoice.pk,
            "status": self.invoice.status,
            "due_date": format_maybe_null_date(self.invoice.date_due),
            "issuance_date": format_maybe_null_date(self.invoice.date_issued),
            "customer_id": {self.customer.id},
            "customer_name": f"{self.customer.first_name}, {self.customer.last_name}",
            "tax": str(self.invoice.sales_tax_percent)
        }
        self.assertEqual(self.invoice.json(), expected_json)
    
    def test_status_choices(self):
        """Test that status can only be set to valid choices"""
        # Test valid choices
        for status in ['created', 'issued', 'paid']:
            self.invoice.status = status
            self.invoice.save()
            self.assertEqual(self.invoice.status, status)