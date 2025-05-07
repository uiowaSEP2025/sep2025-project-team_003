import os
import base64
import unittest
from unittest.mock import Mock, MagicMock, patch
from django.http import HttpResponse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from hsabackend.models.job import Job

from hsabackend.views.generate_quote_pdf_view import (
    _build_quote_pdf,
    generate_quote_pdf,
    generate_quote_pdf_as_base64,
    sign_the_quote,
    send_quote_pdf_to_customer_email,
    get_list_of_quotes_by_org,
    retrieve_quote,
    accept_reject_quote,
)


# ------------------------------------------------------------------ #

#  1. Helper / internal-only tests
# ------------------------------------------------------------------ #
class PDFBuilderTests(unittest.TestCase):
    @patch("hsabackend.views.generate_quote_pdf_view.get_job_detailed_table")
    def test_build_quote_pdf_minimal(self, details):
        """Smoke-test that _build_quote_pdf returns real PDF bytes."""
        fake_job = Mock(
            pk=42,
            customer=Mock(
                last_name="Doe",
                first_name="Jane",
                email="jane@example.com",
                pk=7,
            ),
            start_date=None,
            end_date=None,
        )
        fake_org = Mock(
            org_name="Acme Corp", org_email="info@acme.com", org_phone="5551234567"
        )

        pdf_bytes = _build_quote_pdf(fake_job, fake_org)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

# ------------------------------------------------------------------ #
#  2. /api/generate/quote/<id>
# ------------------------------------------------------------------ #
class GenerateQuotePdfAPITests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.generate_quote_pdf_view.Job.objects.select_related')
    def test_gen_quote_no_job(self, job, org):
        request = self.factory.get("/api/generate/quote/5")
        request.user = Mock(is_authenticated=True)

        mock_org = Mock()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_select_related = Mock()
        job.return_value = mock_select_related
        mock_select_related.get.side_effect = Job.DoesNotExist

        resp = generate_quote_pdf(request, 5)

        assert resp.status_code == 404


    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch("hsabackend.views.generate_quote_pdf_view.Job")
    @patch("hsabackend.views.generate_quote_pdf_view.format_title_case")
    @patch("hsabackend.views.generate_quote_pdf_view._build_quote_pdf")
    def test_generate_quote_pdf_success(
        self, mock_build, mock_format, mock_job, org
    ):
        request = self.factory.get("/api/generate/quote/5")
        request.user = Mock(is_authenticated=True)
        mock_org = Mock()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        mock_org.return_value = mock_org
        fake_job = Mock(pk=5, customer=Mock())
        qs = MagicMock()
        qs.exists.return_value = True
        qs.__getitem__.return_value = fake_job
        mock_job.objects.select_related.return_value.filter.return_value = qs

        mock_build.return_value = b"PDFDATA"
        resp = generate_quote_pdf(request, 5)

        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp["Content-Type"], "application/pdf")
        self.assertIn("Content-Disposition", resp)


# ------------------------------------------------------------------ #
#  3. /api/ret/quote/<id>   (base-64 endpoint)
# ------------------------------------------------------------------ #
class GenerateBase64Tests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch("hsabackend.views.generate_quote_pdf_view.decode")
    @patch("hsabackend.views.generate_quote_pdf_view.Job.objects.get")
    @patch("hsabackend.utils.auth_wrapper.Organization.objects.get")
    def test_base64_not_found(self, org, mock_job, mock_pin):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Mock()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        mock_job.side_effect = Job.DoesNotExist
        mock_pin.return_value="OOga booga"
        request = self.factory.post("/api/ret/quote/100", {"pin": "0000"}, format="json")
        request.user = mock_user
        resp = generate_quote_pdf_as_base64(request, 1)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    @patch("hsabackend.views.generate_quote_pdf_view.decode")
    @patch("hsabackend.views.generate_quote_pdf_view.Job")
    @patch("hsabackend.utils.auth_wrapper.Organization.objects.get")
    def test_base64_invalid_pin(self, org, mock_job, mock_pin):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Mock()
        mock_org.is_onboarding = False
        org.return_value = mock_org

        job = Mock(quote_s3_link=None)
        mock_job.objects.get.return_value = job
        mock_pin.return_value = "oogabooga FAIL"
        request = self.factory.post("/api/ret/quote/1", {"pin": "0000"}, format="json")
        request.user = mock_user
        resp = generate_quote_pdf_as_base64(request, 1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    @patch("hsabackend.views.generate_quote_pdf_view.decode")
    @patch("hsabackend.views.generate_quote_pdf_view.Job")
    @patch("hsabackend.utils.auth_wrapper.Organization.objects.get")
    def test_base64_already_generated(self, org, mock_job, mock_pin):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Mock()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        job = Mock(quote_s3_link="link.pdf")
        mock_job.objects.get.return_value = job
        mock_pin.return_value = job.jwt_json()
        request = self.factory.post("/api/ret/quote/1", {"pin": "1234"}, format="json")
        request.user = mock_user
        resp = generate_quote_pdf_as_base64(request, 1)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("link", resp.data)

    @patch("hsabackend.views.generate_quote_pdf_view._build_quote_pdf")
    @patch("hsabackend.views.generate_quote_pdf_view.decode")
    @patch("hsabackend.views.generate_quote_pdf_view.Job")
    @patch("hsabackend.utils.auth_wrapper.Organization.objects.get")
    def test_base64_success(self, org, mock_job, mock_pin, mock_build):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_org = Mock()
        mock_org.is_onboarding = False
        org.return_value = mock_org
        
        job = Mock(quote_s3_link=None)
        mock_job.objects.get.return_value = job
        mock_pin.return_value = job.jwt_json()
        raw = b"PDF_RAW"
        mock_build.return_value = raw

        request = self.factory.post("/api/ret/quote/1", {"pin": "9999"}, format="json")
        request.user = mock_user
        resp = generate_quote_pdf_as_base64(request, 1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(base64.b64decode(resp.data["quote_pdf_base64"]), raw)


# # ------------------------------------------------------------------ #
# #  4. /api/quote/sign/<id>
# # ------------------------------------------------------------------ #
# class SignTheQuoteTests(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         os.environ.pop("AWS_BUCKET", None)

#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_sign_missing_pdf(self, mock_job):
#         mock_job.objects.get.return_value = Mock()
#         request = self.factory.post("/api/quote/sign/1", {})
#         resp = sign_the_quote(request, 1)
#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_sign_invalid_base64(self, mock_job):
#         mock_job.objects.get.return_value = Mock()
#         request = self.factory.post(
#             "/api/quote/sign/1", {"signed_pdf_base64": "!!!"}
#         )
#         resp = sign_the_quote(request, 1)
#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_sign_no_bucket(self, mock_job):
#         mock_job.objects.get.return_value = Mock()
#         pdf_b64 = base64.b64encode(b"A").decode()
#         request = self.factory.post(
#             "/api/quote/sign/1", {"signed_pdf_base64": pdf_b64}
#         )
#         resp = sign_the_quote(request, 1)
#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#     @patch("hsabackend.views.generate_quote_pdf_view.boto3.client")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_sign_success(self, mock_job, mock_client):
#         os.environ["AWS_BUCKET"] = "bucket"
#         job = Mock(pk=11, quote_s3_link=None, quote_status=None, save=Mock())
#         mock_job.objects.get.return_value = job
#         client = MagicMock()
#         client.put_object.return_value = {}
#         mock_client.return_value = client

#         pdf_b64 = base64.b64encode(b"PDF").decode()
#         request = self.factory.post(
#             "/api/quote/sign/11", {"signed_pdf_base64": pdf_b64}
#         )
#         resp = sign_the_quote(request, 11)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertTrue(resp.data["quote_s3_link"].startswith("quotes/quote_11_signed_"))


# # ------------------------------------------------------------------ #
# #  5. /api/quotes list + accept/reject
# # ------------------------------------------------------------------ #
# class GetListOfQuotesByOrgTests(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()

#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_invalid_filter(self, mock_job, mock_org):
#         mock_org.objects.get.return_value = Mock()
#         request = self.factory.get("/api/quotes?filterby=foo")
#         resp = get_list_of_quotes_by_org(request)
#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_success(self, mock_job, mock_org):
#         mock_org.objects.get.return_value = Mock()
#         mock_job.objects.select_related.return_value.filter.return_value = []
#         request = self.factory.get("/api/quotes")
#         resp = get_list_of_quotes_by_org(request)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)


# class AcceptRejectQuoteTests(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()

#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_invalid_decision(self, mock_job, mock_org):
#         mock_org.objects.get.return_value = Mock()
#         job = Mock(quote_status="created")
#         mock_job.objects.select_related.return_value.get.return_value = job
#         request = self.factory.post(
#             "/api/quotes/2/accept_reject/", {"decision": "foo"}
#         )
#         resp = accept_reject_quote(request, 2)
#         self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

# # ------------------------------------------------------------------ #
# #  6. Extra list / retrieve / accept‑reject branches for coverage
# # ------------------------------------------------------------------ #

# class GetListFilteredTests(APITestCase):
#     """Covers lines 246‑281: filter=created branch and result rendering."""
#     def setUp(self):
#         self.factory = APIRequestFactory()

#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_filter_created(self, mock_job, mock_org):
#         mock_org.objects.get.return_value = Mock()
#         j = Mock(
#             pk=9,
#             customer=Mock(first_name="Ann", last_name="Lee"),
#             quote_status="created",
#             quote_s3_link=None,
#             start_date=None,
#             end_date=None,
#         )
#         # First .filter() is for organization, second is the status filter
#         mock_job.objects.select_related.return_value.filter.return_value.filter.return_value = [j]

#         request = self.factory.get("/api/quotes?filterby=created")
#         resp = get_list_of_quotes_by_org(request)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(resp.data["data"][0]["job_id"], 9)
#         self.assertEqual(resp.data["data"][0]["quote_status"], "created")


# class RetrieveQuoteEndpointVariants(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         os.environ["AWS_BUCKET"] = "mybucket"
#         os.environ["AWS_ENDPOINT"] = "https://s3.example.com"

#     def tearDown(self):
#         os.environ.pop("AWS_ENDPOINT", None)
#         os.environ.pop("AWS_BUCKET", None)

#     @patch("hsabackend.views.generate_quote_pdf_view.boto3.client")
#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_retrieve_success_with_endpoint(self, mock_job, mock_org, mock_client):
#         mock_org.objects.get.return_value = Mock()
#         job = Mock(quote_s3_link="key")
#         mock_job.objects.select_related.return_value.get.return_value = job
#         client = MagicMock()
#         client.generate_presigned_url.return_value = "https://signed.example.com/k"
#         mock_client.return_value = client

#         request = self.factory.get("/api/quotes/99/retrieve")
#         resp = retrieve_quote(request, 99)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(resp.data["url"], "https://signed.example.com/k")
#         # ensure the custom endpoint path was exercised
#         mock_client.assert_called_once_with(
#             service_name="s3",
#             endpoint_url="https://s3.example.com",
#             region_name="auto",
#         )


# class AcceptRejectHappyPathTests(APITestCase):
#     """Hits lines 390‑420: both ‘accept’ and ‘reject’ branches."""
#     def setUp(self):
#         self.factory = APIRequestFactory()

#     @patch("hsabackend.views.generate_quote_pdf_view.accept_reject_quote")
#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_accept_flow(self, mock_job, mock_org, mock_email):
#         mock_org.objects.get.return_value = Mock()
#         cust = Mock(first_name="Bo", email="bo@x")
#         job = Mock(pk=44, quote_status="created", customer=cust, save=Mock())
#         mock_job.objects.select_related.return_value.get.return_value = job
#         mock_email.return_value = Mock(send=Mock())

#         request = self.factory.post("/api/quotes/44/accept_reject/", {"decision": "accept"})
#         resp = accept_reject_quote(request, 44)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(resp.data["quote_status"], "accepted")
#         job.save.assert_called_once()

#     @patch("hsabackend.views.generate_quote_pdf_view.accept_reject_quotes")
#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_reject_flow(self, mock_job, mock_org, mock_email):
#         mock_org.objects.get.return_value = Mock()
#         cust = Mock(first_name="Cy", email="cy@y")
#         job = Mock(pk=55, quote_status="created", customer=cust, save=Mock())
#         mock_job.objects.select_related.return_value.get.return_value = job
#         mock_email.return_value = Mock(send=Mock())

#         request = self.factory.post("/api/quotes/55/accept_reject/", {"decision": "reject"})
#         resp = accept_reject_quote(request, 55)
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         # self.assertEqual(resp.data["quote_status"], "rejected") all of this is done in the Mail util fn that is patched
#         # quote_s3_link should be nulled out in reject path
#         # job.save.assert_called_once()
#         # self.assertIsNone(job.quote_s3_link)
# class PDFBuilderWithDataTests(unittest.TestCase):

#     @patch("hsabackend.views.generate_quote_pdf_view.FPDF")
#     def test_build_pdf_with_services_and_materials(self, mock_fpdf):
#         # ---------- 1. stub out a VERY thin FPDF replacement ----------
#         pdf_stub = MagicMock()
#         pdf_stub.w = 200
#         pdf_stub.l_margin = 10
#         pdf_stub.r_margin = 10
#         pdf_stub.get_y.return_value = 50

#         # Provide a fake context‑manager for pdf.table()
#         row_stub = MagicMock()
#         tbl_stub = MagicMock(row=MagicMock(return_value=row_stub))
#         cm = MagicMock(__enter__=MagicMock(return_value=tbl_stub), __exit__=MagicMock())
#         pdf_stub.table.return_value = cm

#         # Make .output(buf) write a dummy PDF header so that the code
#         # that inspects the returned value still sees “%PDF”.
#         def _output(buf):
#             buf.write(b"%PDF")
#         pdf_stub.output.side_effect = _output

#         mock_fpdf.return_value = pdf_stub

#         # ---------- 3. build the PDF ----------
#         job = Mock(
#             pk=1,
#             customer=Mock(first_name="Al", last_name="Smith", email="al@smith"),
#             start_date=None,
#             end_date=None,
#         )
#         org = Mock(org_name="Widgets Inc", org_email="info@widgets", org_phone="5551112222")

#         pdf_bytes = _build_quote_pdf(job, org)

#         # ---------- 4. assertions ----------
#         self.assertTrue(pdf_bytes.startswith(b"%PDF"))
#         # one table for services + one for materials
#         self.assertEqual(pdf_stub.table.call_count, 2)
#         # each “row” call executed at least once (header + data rows)

#         self.assertGreaterEqual(tbl_stub.row.call_count, 2)

# class SendQuotePDFEmailTests(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         # ensure EMAIL_HOST_USER is set
#         os.environ['EMAIL_HOST_USER'] = 'no-reply@hsa.com'

#     def tearDown(self):
#         os.environ.pop('EMAIL_HOST_USER', None)

#     def test_send_quote_unauthenticated(self):
#         request = self.factory.post('/api/send/quote/1')
#         request.user = Mock(is_authenticated=False)

#         resp = send_quote_pdf_to_customer_email(request, 1)
#         self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(resp.data, {"message": "Invalid credentials"})

#     @patch("hsabackend.views.generate_quote_pdf_view._build_quote_pdf")
#     @patch("hsabackend.views.generate_quote_pdf_view.send_quotes_email")
#     @patch("hsabackend.views.generate_quote_pdf_view.Organization")
#     @patch("hsabackend.views.generate_quote_pdf_view.Job")
#     def test_send_quote_success(self, mock_job, mock_org, mock_email_class, mock_build):
#         # prepare request and user
#         request = self.factory.post('/api/send/quote/3')
#         request.user = Mock(is_authenticated=True, pk=7)

#         # stub Organization.get
#         org = Mock(pk=20)
#         mock_org.objects.get.return_value = org

#         # stub Job lookup
#         cust = Mock(first_name="Dana", email="dana@example.com")
#         job = Mock(pk=3, customer=cust)
#         mock_job.objects.select_related.return_value.get.return_value = job

#         # stub PDF bytes and PIN
#         pdf_data = b'PDFDATA'
#         mock_build.return_value = pdf_data

#         # stub EmailMultiAlternatives instance
#         email_msg = Mock(attach_alternative=Mock(), attach=Mock(), send=Mock())
#         mock_email_class.return_value = "alex.t.guo@gmail.com"

#         resp = send_quote_pdf_to_customer_email(request, 3)

#         # assertions
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         self.assertEqual(resp.data, {"message": f"Quote PDF sent to alex.t.guo@gmail.com"})
#         # PDF builder called with correct args
#         mock_build.assert_called_once_with(job, org)
