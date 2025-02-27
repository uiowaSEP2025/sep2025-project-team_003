from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

import hsabackend.views.index as hview
from hsabackend.views.user_auth import login_view
from hsabackend.views.customers import get_customer_table_data,create_customer,edit_customer, delete_customer
from hsabackend.views.requests import get_org_request_data,delete_request

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # auth
    path("api/login", login_view),

    # customer
    path("api/get/customers", get_customer_table_data),
    path("api/create/customer", create_customer),
    path("api/edit/customer/<int:id>", edit_customer),
    path("api/delete/customer/<int:id>", delete_customer),

    # request
    path("api/get/request", get_org_request_data),
    path("api/delete/request/<int:id>", delete_customer),

    # all non API routes should redirect to angular
    # must be at the bottom!!!
    re_path(r'.*', hview.main_view)   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
