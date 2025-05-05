# hsabackend/tests/test_generate_requests_iframe_view.py

import os
from django.test import TestCase
from django.http import HttpResponse, Http404
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock

from hsabackend.views.generate_requests_iframe import get_html_form, get_url
from hsabackend.models.organization import Organization


class GetURLTests(TestCase):
    def test_default_env_returns_localhost(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_url(), "http://localhost:8000")

    def test_dev_env_returns_dev_url(self):
        with patch.dict(os.environ, {"ENV": "DEV"}, clear=True):
            self.assertEqual(get_url(), "https://hsa.ssankey.com")

    def test_prod_env_returns_prod_url(self):
        with patch.dict(os.environ, {"ENV": "PROD"}, clear=True):
            self.assertEqual(get_url(), "https://hsa-app.starlitex.com")

    def test_invalid_env_raises_runtime_error(self):
        with patch.dict(os.environ, {"ENV": "STAGING"}, clear=True):
            with self.assertRaises(RuntimeError):
                get_url()


class GenerateRequestsIframeViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('hsabackend.views.generate_requests_iframe.get_url')
    @patch('hsabackend.views.generate_requests_iframe.render')
    @patch('hsabackend.views.generate_requests_iframe.Contractor.objects.filter')
    @patch('hsabackend.views.generate_requests_iframe.Service.objects.filter')
    @patch('hsabackend.views.generate_requests_iframe.get_object_or_404')
    def test_getHTMLForm_success(self,
                                 mock_get_404,
                                 mock_service_filter,
                                 mock_contractor_filter,
                                 mock_render,
                                 mock_get_url):

        org = Organization(pk=42)
        mock_get_404.return_value = org
        mock_get_url.return_value = "http://testserver"
        mock_service_filter.return_value = ['svcA', 'svcB']
        mock_contractor_filter.return_value =  ['ctrX']

        fake_resp = HttpResponse(b"OK")
        fake_resp.headers = {'X-Frame-Options': 'SAMEORIGIN'}
        mock_render.return_value = fake_resp

        request = self.factory.get('/api/request/genhtml/42')
        response = get_html_form(request, 42)

        mock_get_404.assert_called_once_with(Organization, pk=42)
        mock_service_filter.assert_called_once_with(organization=org)
        mock_contractor_filter.assert_called_once_with(organization=org)

        expected_context = {
            'url': 'http://testserver/api/create/request/42',
            'org_id': 42,
            'services': ['svcA', 'svcB'],
            'contractors': ['ctrX'],
        }

        self.assertNotIn('X-Frame-Options', response.headers)
        self.assertEqual(response.content, b"OK")
