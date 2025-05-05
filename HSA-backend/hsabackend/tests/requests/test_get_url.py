import os
from unittest.mock import patch

from django.test import TestCase

from hsabackend.views.generate_requests_iframe import get_url


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
