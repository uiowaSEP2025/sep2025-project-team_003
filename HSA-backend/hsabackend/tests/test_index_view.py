from django.test import TestCase, Client
from django.urls import reverse

class IndexViewTest(TestCase):
    """Test cases for the Index view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.index_url = reverse('main_view')
    
    def test_index_view_renders_template(self):
        """Test that the index view renders the correct template"""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_index_view_context(self):
        """Test that the index view provides the correct context"""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['static_url'], '/static')
    
    def test_index_view_sets_csrf_cookie(self):
        """Test that the index view sets a CSRF cookie"""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.cookies.get('csrftoken'))