from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

import hsabackend.views.index as hview
from hsabackend.views.user_auth import login_view
from hsabackend.views.customers import get_customer_table_data,create_customer

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    
    path("api/login", login_view),
    path("api/get/customers", get_customer_table_data),
    path("api/create/customer", create_customer),

    # all non API routes should redirect to angular
    # must be at the bottom!!!
    re_path(r'.*', hview.main_view)   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
