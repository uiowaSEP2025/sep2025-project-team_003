# hsabackend/tests/test_generate_requests_iframe_view.py

import os
from django.test import TestCase
from django.http import HttpResponse, Http404
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock

from hsabackend.views.generate_requests_iframe import getHTMLForm, get_url
from hsabackend.models.organization import Organization


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
        response = getHTMLForm(request, 42)

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
