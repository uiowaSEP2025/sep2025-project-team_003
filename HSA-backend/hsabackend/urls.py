from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponseNotFound
import hsabackend.views.index as hview
from hsabackend.views.contractors_list import ContractorsList
from hsabackend.views.user_auth import login_view, logout_view
from hsabackend.views.customers import get_customer_excluded_table_data, get_customer_table_data, create_customer, edit_customer, delete_customer
from hsabackend.views.contractors import get_contractor_excluded_table_data, get_contractor_table_data, create_contractor, edit_contractor, delete_contractor
from hsabackend.views.requests import get_org_request_data, delete_request,approve_request
from hsabackend.views.services import get_service_table_data, get_service_excluded_table_data, create_service, edit_service, delete_service
from hsabackend.views.materials import get_material_excluded_table_data, get_material_table_data, create_material, edit_material, delete_material
from hsabackend.views.invoices import createInvoice, getInvoices, deleteInvoice, updateInvoice, get_data_for_invoice
from hsabackend.views.jobs import get_job_table_data, get_job_individual_data, create_job, edit_job, delete_job
from hsabackend.views.jobs_services import get_job_service_table_data, create_job_service, delete_job_service, delete_cached_job_service
from hsabackend.views.jobs_materials import get_job_material_table_data, create_job_material, delete_job_material, delete_cached_job_material
from hsabackend.views.jobs_contractors import get_job_contractor_table_data, create_job_contractor, delete_job_contractor, delete_cached_job_contractor
from hsabackend.views.job_templates import get_job_template_table_data, get_job_template_individual_data, create_job_template, edit_job_template, delete_job_template
from hsabackend.views.job_templates_services import get_job_template_service_table_data, create_job_template_service, delete_job_template_service, delete_cached_job_template_service
from hsabackend.views.job_templates_materials import get_job_template_material_table_data, create_job_template_material, delete_job_template_material, delete_cached_job_template_material
from hsabackend.views.invoices import createInvoice, getInvoices, deleteInvoice, updateInvoice
from hsabackend.views.quotes import getQuotesForInvoiceByCustomer, getQuotesForInvoiceByInvoice
from hsabackend.views.generate_invoice_pdf_view import generate_pdf
from hsabackend.views.organizations import createOrganization, deleteOrganization, getOrganizationDetail, editOrganizationDetail
from hsabackend.views.discounts import get_discounts, edit_discount, create_discount, delete_discount
from django.http import HttpResponse

def handle_unmatched_api(request):
    return HttpResponseNotFound("404 Not Found")

def handle_health_check(request):
    return HttpResponse("OK", content_type="text/plain", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),

    # health check (used for int testing)
    path("api/healthcheck", handle_health_check),

    # auth
    path("api/login", login_view),
    path("api/logout", logout_view),

    # customer
    path("api/get/customers", get_customer_table_data),
    path("api/get/customers/exclude", get_customer_excluded_table_data),
    path("api/create/customer", create_customer),
    path("api/edit/customer/<int:id>", edit_customer),
    path("api/delete/customer/<int:id>", delete_customer),

    # contractor
    path("api/get/contractors", ContractorsList.as_view(), name="get-contractors"),
    path("api/get/contractors/exclude", get_contractor_excluded_table_data),
    path("api/create/contractor", create_contractor),
    path("api/edit/contractor/<int:id>", edit_contractor),
    path("api/delete/contractor/<int:id>", delete_contractor),

    # request
    path("api/get/requests", get_org_request_data),
    path("api/delete/request/<int:id>", delete_request),
    path("api/approve/request/<int:id>", approve_request),

    # service 
    path("api/get/services", get_service_table_data),
    path("api/get/services/exclude", get_service_excluded_table_data),
    path("api/create/service", create_service),
    path("api/edit/service/<int:id>", edit_service),
    path("api/delete/service/<int:id>", delete_service),

    # materials
    path("api/get/materials", get_material_table_data),
    path("api/get/materials/exclude", get_material_excluded_table_data),
    path("api/create/material", create_material),
    path("api/edit/material/<int:id>", edit_material),
    path("api/delete/material/<int:id>", delete_material),

    # jobs
    path("api/get/jobs", get_job_table_data),
    path("api/get/job/<int:id>", get_job_individual_data),
    path("api/create/job", create_job),
    path("api/edit/job/<int:id>", edit_job),
    path("api/delete/job/<int:id>", delete_job),

    # jobs_services join
    path("api/get/job/<int:id>/services", get_job_service_table_data),
    path("api/create/job/<int:id>/service", create_job_service),
    path("api/delete/job/<int:job_id>/service/<int:job_service_id>", delete_job_service),
    path("api/delete/job/<int:job_id>/services", delete_cached_job_service),

    # jobs_materials join
    path("api/get/job/<int:id>/materials", get_job_material_table_data),
    path("api/create/job/<int:id>/material", create_job_material),
    path("api/delete/job/<int:job_id>/material/<int:job_material_id>", delete_job_material),
    path("api/delete/job/<int:job_id>/materials", delete_cached_job_material),

    # jobs_contractors join
    path("api/get/job/<int:id>/contractors", get_job_contractor_table_data),
    path("api/create/job/<int:id>/contractor", create_job_contractor),
    path("api/delete/job/<int:job_id>/contractor/<int:job_contractor_id>", delete_job_contractor),
    path("api/delete/job/<int:job_id>/contractors", delete_cached_job_contractor),

    # job_templates
    path("api/get/jobtemplates", get_job_template_table_data),
    path("api/get/jobtemplate/<int:id>", get_job_template_individual_data),
    path("api/create/jobtemplate", create_job_template),
    path("api/edit/jobtemplate/<int:id>", edit_job_template),
    path("api/delete/jobtemplate/<int:id>", delete_job_template),

    # job_templates_services join
    path("api/get/jobtemplate/<int:id>/services", get_job_template_service_table_data),
    path("api/create/jobtemplate/<int:id>/service", create_job_template_service),
    path("api/delete/jobtemplate/<int:job_template_id>/service/<int:job_template_service_id>", delete_job_template_service),
    path("api/delete/jobtemplate/<int:job_template_id>/services", delete_cached_job_template_service),

    # job_templates_materials join
    path("api/get/jobtemplate/<int:id>/materials", get_job_template_material_table_data),
    path("api/create/jobtemplate/<int:id>/material", create_job_template_material),
    path("api/delete/jobtemplate/<int:job_template_id>/material/<int:job_template_material_id>", delete_job_template_material),
    path("api/delete/jobtemplate/<int:job_template_id>/materials", delete_cached_job_template_material),

    # invoices
    path("api/create/invoice", createInvoice),
    path("api/get/invoices", getInvoices),
    path("api/delete/invoice/<int:id>", deleteInvoice),
    path("api/edit/invoice/<int:id>", updateInvoice),
    path("api/generate/invoice/<int:id>", generate_pdf),
    path("api/get/invoice/displaydata/<int:id>", get_data_for_invoice),
    
    # orgs
    path("api/create/organization", createOrganization),
    path("api/get/organization", getOrganizationDetail),
    path("api/edit/organization", editOrganizationDetail),
    path("api/delete/organization", deleteOrganization),

    # quotes
    path("api/get/quotesforinvoice/customer/<int:id>", getQuotesForInvoiceByCustomer),
    path("api/get/quotesforinvoice/invoice/<int:id>", getQuotesForInvoiceByInvoice),

    # discounts
    path("api/get/discounts", get_discounts),
    path("api/edit/discount/<int:id>", edit_discount),
    path("api/create/discount", create_discount),
    path("api/delete/discount/<int:id>", delete_discount),

    # Catch-all for unmatched API requests
    re_path(r'^api/.*', handle_unmatched_api), 

    # all non API routes should redirect to angular
    # must be at the bottom!!!
    re_path(r'.*', hview.main_view)   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
