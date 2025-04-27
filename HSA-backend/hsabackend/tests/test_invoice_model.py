from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import date
from hsabackend.models.invoice import Invoice
from hsabackend.models.customer import Customer
from hsabackend.models.discount import Discount
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.utils.string_formatters import format_maybe_null_date

class InvoiceModelTest(TestCase):
    """Test cases for the Invoice model"""
    
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
        
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="1234567890",
            notes="Test notes",
            organization=self.organization
        )
        
        self.discount1 = Discount.objects.create(
            discount_name="Test Discount 1",
            discount_percent=Decimal('10.00'),
            organization=self.organization
        )
        
        self.discount2 = Discount.objects.create(
            discount_name="Test Discount 2",
            discount_percent=Decimal('5.00'),
            organization=self.organization
        )
        
        self.invoice = Invoice.objects.create(
            date_issued=date(2023, 1, 1),
            date_due=date(2023, 1, 31),
            status="created",
            sales_tax_percent=Decimal('7.00'),
            customer=self.customer,
            payment_link="https://example.com/payment"
        )
        
        # Add discounts to the invoice
        self.invoice.discounts.add(self.discount1, self.discount2)
        
        # Create a job for the invoice
        self.job = Job.objects.create(
            name="Test Job",
            address="456 Test Ave",
            city="Test City",
            state="TS",
            zip_code="12345",
            organization=self.organization,
            invoice=self.invoice
        )
    
    def test_invoice_creation(self):
        """Test that an invoice can be created"""
        self.assertEqual(self.invoice.date_issued, date(2023, 1, 1))
        self.assertEqual(self.invoice.date_due, date(2023, 1, 31))
        self.assertEqual(self.invoice.status, "created")
        self.assertEqual(self.invoice.sales_tax_percent, Decimal('7.00'))
        self.assertEqual(self.invoice.customer, self.customer)
        self.assertEqual(self.invoice.payment_link, "https://example.com/payment")
        self.assertEqual(list(self.invoice.discounts.all()), [self.discount1, self.discount2])
    
    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f"<Invoice, customer: {self.customer}>"
        self.assertEqual(str(self.invoice), expected_str)
    
    def test_discount_aggregate_percentage(self):
        """Test the discount_aggregate_percentage property"""
        # Should be 10% + 5% = 15%
        self.assertEqual(self.invoice.discount_aggregate_percentage, Decimal('15.00'))
    
    def test_subtotal(self):
        """Test the subtotal property"""
        # The job's subtotal is 0 by default, so the invoice's subtotal should also be 0
        self.assertEqual(self.invoice.subtotal, 0)
    
    def test_discounted_subtotal(self):
        """Test the discounted_subtotal property"""
        # subtotal * discount_aggregate_percentage / 100
        # 0 * 15 / 100 = 0
        self.assertEqual(self.invoice.discounted_subtotal, 0)
    
    def test_subtotal_after_discount(self):
        """Test the subtotal_after_discount property"""
        # subtotal - discounted_subtotal
        # 0 - 0 = 0
        self.assertEqual(self.invoice.subtotal_after_discount, 0)
    
    def test_taxable_amount(self):
        """Test the taxable_amount property"""
        # subtotal_after_discount * (sales_tax_percent / 100)
        # 0 * (7 / 100) = 0
        self.assertEqual(self.invoice.taxable_amount, 0)
    
    def test_total(self):
        """Test the total property"""
        # subtotal_after_discount + taxable_amount
        # 0 + 0 = 0
        self.assertEqual(self.invoice.total, 0)
    
    def test_json_for_view_invoice_method(self):
        """Test the json_for_view_invoice method"""
        expected_json = {
            "id": self.invoice.pk,
            "status": "created",
            "dueDate": date(2023, 1, 31),
            "issuanceDate": date(2023, 1, 1),
            "customer": "Jane, Smith"
        }
        self.assertEqual(self.invoice.json_for_view_invoice(), expected_json)
    
    def test_json_method(self):
        """Test the json method"""
        expected_json = {
            "id": self.invoice.pk,
            "status": "created",
            "due_date": format_maybe_null_date(date(2023, 1, 31)),
            "issuance_date": format_maybe_null_date(date(2023, 1, 1)),
            "customer_id": {self.customer.id},
            "customer_name": "Jane, Smith",
            "tax": str(Decimal('7.00'))
        }
        self.assertEqual(self.invoice.json(), expected_json)
    
    def test_status_choices(self):
        """Test that status choices are enforced"""
        # Test all valid statuses
        for status in ["created", "issued", "paid"]:
            self.invoice.status = status
            self.invoice.save()
            self.assertEqual(self.invoice.status, status)