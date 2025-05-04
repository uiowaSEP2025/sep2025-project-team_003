from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.urls import path, re_path, include

import hsabackend.views.index as hview
from hsabackend.views.bookings import create_event, delete_event, edit_event, get_booking_data
from hsabackend.views.contractors import get_contractor_excluded_table_data, get_contractor_table_data, \
    create_contractor, edit_contractor, delete_contractor, get_all_contractors_for_org
from hsabackend.views.customers import get_customer_excluded_table_data, get_customer_table_data, create_customer, \
    edit_customer, delete_customer
from hsabackend.views.discounts import get_discounts, edit_discount, create_discount, delete_discount
from hsabackend.views.generate_invoice_pdf_view import generate_invoice_pdf
from hsabackend.views.generate_quote_pdf_view import generate_quote_pdf, send_quote_pdf_to_customer_email
from hsabackend.views.generate_requests_iframe import getHTMLForm
from hsabackend.views.invoices import create_invoice, get_invoices, delete_invoice, update_invoice, \
    get_data_for_invoice, get_invoice, get_quotes_for_invoice_by_customer
from hsabackend.views.job_templates import get_job_template_table_data, get_job_template_individual_data, \
    create_job_template, edit_job_template, delete_job_template
from hsabackend.views.job_templates_materials import get_job_template_material_table_data, create_job_template_material, \
    delete_job_template_material, delete_cached_job_template_material
from hsabackend.views.job_templates_services import get_job_template_service_table_data, create_job_template_service, \
    delete_job_template_service, delete_cached_job_template_service
from hsabackend.views.jobs import get_job_excluded_table_data, get_job_table_data, get_job_individual_data, create_job, \
    edit_job, delete_job, get_jobs_by_contractor
from hsabackend.views.materials import get_material_excluded_table_data, get_material_table_data, create_material, \
    edit_material, delete_material
from hsabackend.views.organizations import complete_onboarding, create_organization, get_organization, \
    edit_organization
from hsabackend.views.requests import get_org_request_data, delete_request, approve_request, create_request
from hsabackend.views.services import get_service_table_data, get_service_excluded_table_data, create_service, \
    edit_service, delete_service
from hsabackend.views.user_auth import login_view, logout_view, user_create, user_exist


def handle_unmatched_api(request):
    return HttpResponseNotFound("404 Not Found")

def handle_health_check(request):
    return HttpResponse("OK", content_type="text/plain", status=200)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    # health check (used for int testing)
    path("api/healthcheck", handle_health_check, name='handle_health_check'),

    # auth
    path("api/login", login_view, name='login_view'),
    path("api/logout", logout_view, name='logout_view'),
    path("api/create/user", user_create, name='user_create'),
    path("api/userexist", user_exist, name='user_exist'),

    # customer
    path("api/get/customers", get_customer_table_data, name='get_customer_table_data'),
    path("api/get/customers/exclude", get_customer_excluded_table_data, name='get_customer_excluded_table_data'),
    path("api/create/customer", create_customer, name='create_customer'),
    path("api/edit/customer/<int:customer_id>", edit_customer, name='edit_customer'),
    path("api/delete/customer/<int:customer_id>", delete_customer, name='delete_customer'),

    # contractor
    path("api/get/all/contractors", get_all_contractors_for_org, name='get_all_contractors_for_org'),
    path("api/get/contractors", get_contractor_table_data, name='get_contractor_table_data'),
    path("api/get/contractors/exclude", get_contractor_excluded_table_data, name='get_contractor_excluded_table_data'),
    path("api/create/contractor", create_contractor, name='create_contractor'),
    path("api/edit/contractor/<int:contractor_id>", edit_contractor, name='edit_contractor'),
    path("api/delete/contractor/<int:contractor_id>", delete_contractor, name='delete_contractor'),

    # request
    path("api/get/requests", get_org_request_data, name='get_org_request_data'),
    path("api/delete/request/<int:request_id>", delete_request, name='delete_request'),
    path("api/create/request/<int:request_id>", create_request, name='create_request'),
    path("api/approve/request/<int:request_id>", approve_request, name='approve_request'),
    path("api/request/genhtml/<int:request_id>", getHTMLForm),

    # service
    path("api/get/services", get_service_table_data, name='get_service_table_data'),
    path("api/get/services/exclude", get_service_excluded_table_data, name='get_service_excluded_table_data'),
    path("api/create/service", create_service, name='create_service'),
    path("api/edit/service/<int:service_id>", edit_service, name='edit_service'),
    path("api/delete/service/<int:service_id>", delete_service, name='delete_service'),

    # materials
    path("api/get/materials", get_material_table_data, name='get_material_table_data'),
    path("api/get/materials/exclude", get_material_excluded_table_data, name='get_material_excluded_table_data'),
    path("api/create/material", create_material, name='create_material'),
    path("api/edit/material/<int:material_id>", edit_material, name='edit_material'),
    path("api/delete/material/<int:material_id>", delete_material, name='delete_material'),

    # jobs
    path("api/get/jobs", get_job_table_data, name='get_job_table_data'),
    path("api/get/jobs/exclude", get_job_excluded_table_data, name='get_job_excluded_table_data'),
    path("api/get/job/<int:job_id>", get_job_individual_data, name='get_job_individual_data'),
    path("api/create/job", create_job, name='create_job'),
    path("api/edit/job/<int:job_id>", edit_job, name='edit_job'),
    path("api/delete/job/<int:job_id>", delete_job, name='delete_job'),
    path("api/get/jobs/by-contractor", get_jobs_by_contractor, name='get_jobs_by_contractor'),

    path("api/generate/quote/<int:job_id>", generate_quote_pdf, name='generate_quote_pdf'),
    path("api/get/quotesforinvoice/customer/<int:customer_id>", get_quotes_for_invoice_by_customer, name="get_quotes_for_invoice_by_customer"),
    path("api/send/quote/<int:job_id>", send_quote_pdf_to_customer_email, name='send_quote_pdf_to_customer_email'),

    # job_templates
    path("api/get/jobtemplates", get_job_template_table_data, name='get_job_template_table_data'),
    path("api/get/jobtemplate/<int:job_template_id>", get_job_template_individual_data, name='get_job_template_individual_data'),
    path("api/create/jobtemplate", create_job_template, name='create_job_template'),
    path("api/edit/jobtemplate/<int:job_template_id>", edit_job_template, name='edit_job_template'),
    path("api/delete/jobtemplate/<int:job_template_id>", delete_job_template, name='delete_job_template'),

    # job_templates_services join
    path("api/get/jobtemplate/<int:job_template_id>/services", get_job_template_service_table_data, name='get_job_template_service_table_data'),
    path("api/create/jobtemplate/<int:job_template_id>/service", create_job_template_service, name='create_job_template_service'),
    path("api/delete/jobtemplate/<int:job_template_id>/service/<int:job_template_service_id>", delete_job_template_service, name='delete_job_template_service'),
    path("api/delete/jobtemplate/<int:job_template_id>/services", delete_cached_job_template_service, name='delete_cached_job_template_service'),

    # job_templates_materials join
    path("api/get/jobtemplate/<int:job_template_id>/materials", get_job_template_material_table_data, name='get_job_template_material_table_data'),
    path("api/create/jobtemplate/<int:job_template_id>/material", create_job_template_material, name='create_job_template_material'),
    path("api/delete/jobtemplate/<int:job_template_id>/material/<int:job_template_material_id>", delete_job_template_material, name='delete_job_template_material'),
    path("api/delete/jobtemplate/<int:job_template_id>/materials", delete_cached_job_template_material, name='delete_cached_job_template_material'),

    # invoices
    path("api/create/invoice", create_invoice, name='create_invoice'),
    path("api/get/invoices", get_invoices, name='get_invoices'),
    path("api/delete/invoice/<int:invoice_id>", delete_invoice, name='delete_invoice'),
    path("api/edit/invoice/<int:invoice_id>", update_invoice, name='update_invoice'),
    path("api/generate/invoice/<int:invoice_id>", generate_invoice_pdf, name='generate_invoice_pdf'),
    path("api/get/invoice/display-data/<int:invoice_id>", get_data_for_invoice, name='get_data_for_invoice'),
    path("api/get/invoice/<int:invoice_id>", get_invoice, name='get_invoice'),

    # orgs
    path("api/create/organization", create_organization, name='create_organization'),
    path("api/get/organization", get_organization, name='get_organization'),
    path("api/edit/organization", edit_organization, name='edit_organization'),
    path("api/edit/organization/onboarding", complete_onboarding, name='complete_onboarding'),


    # discounts
    path("api/get/discounts", get_discounts, name='get_discounts'),
    path("api/edit/discount/<int:discount_id>", edit_discount, name='edit_discount'),
    path("api/create/discount", create_discount, name='create_discount'),
    path("api/delete/discount/<int:discount_id>", delete_discount, name='delete_discount'),

    # bookings
    path("api/get/bookings", get_booking_data, name="get_booking_data"),
    path("api/create/booking", create_event, name='create_event'),
    path("api/edit/booking/<int:booking_id>", edit_event, name='edit_event'),
    path("api/delete/booking/<int:booking_id>", delete_event, name='delete_event'),

    # password reset
    re_path(r'^api/password_reset/', include('hsabackend.utils.password_reset_route_adder', namespace='password_reset'), name='password_reset'),

    # Catch-all for unmatched API requests
    re_path(r'^api/.*', handle_unmatched_api, name='handle_unmatched_api'),

    # all non-API routes should redirect to angular
    # must be at the bottom!!!
    re_path(r'.*', hview.main_view, name='main_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
