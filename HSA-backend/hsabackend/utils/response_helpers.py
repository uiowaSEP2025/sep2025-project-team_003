from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils import json

from hsabackend.models.booking import Booking
from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.discount import Discount
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job, JobsServices, JobsMaterials
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from hsabackend.models.organization import Organization
from hsabackend.models.request import Request
from hsabackend.models.service import Service
from hsabackend.serializers.booking_serializer import BookingSerializer
from hsabackend.serializers.contractor_serializer import ContractorSerializer, ContractorTableSerializer
from hsabackend.serializers.customer_serializer import CustomerSerializer, CustomerTableSerializer
from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.serializers.invoice_serializer import InvoiceSerializer
from hsabackend.serializers.job_serializer import JobSerializer, JobTableSerializer
from hsabackend.serializers.job_template_serializer import JobTemplateSerializer
from hsabackend.serializers.material_serializer import MaterialSerializer
from hsabackend.serializers.organization_serializer import OrganizationSerializer
from hsabackend.serializers.request_serializer import RequestSerializer
from hsabackend.serializers.service_serializer import ServiceSerializer


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'pagesize'
    page_query_param = 'offset'

    def get_page_number(self, request, paginator):
        # Get the page number from the request
        page_number = request.query_params.get(self.page_query_param, 0)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            # In the original implementation, offset is 0-indexed
            # Django's pagination is 1-indexed, so we add 1
            return int(page_number) + 1
        except (TypeError, ValueError):
            return 1

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'totalCount': self.page.paginator.count
        })


def get_table_data(request, object_type, exclude=False):
    search = request.query_params.get('search', '')
    paginator = CustomPagination()

    if exclude:
        excluded_ids_str = request.GET.getlist('excludeIDs', [])
        exclude_ids = [int(id) for id in excluded_ids_str]

    match object_type:
        case "job_template":
            queryset = JobTemplate.objects.filter(organization=request.organization.pk).order_by('name')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )

            page = paginator.paginate_queryset(queryset, request)
            serializer = JobTemplateSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "contractor":
            queryset = Contractor.objects.filter(organization=request.organization.pk).order_by('first_name')
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search)
                )

            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])

            page = paginator.paginate_queryset(queryset, request)
            serializer = ContractorTableSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "customer":
            queryset = Customer.objects.filter(organization=request.organization.pk).order_by('first_name')
            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = CustomerTableSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "job":
            queryset = Job.objects.filter(organization=request.organization.pk).order_by('start_date')
            if search:
                queryset = queryset.filter(
                    Q(customer__first_name__icontains=search) |
                    Q(customer__last_name__icontains=search) |
                    Q(start_date__icontains=search) |
                    Q(end_date__icontains=search) |
                    Q(job_status__icontains=search) |
                    Q(description__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = JobTableSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "service":
            queryset = Service.objects.filter(organization=request.organization.pk).order_by('name')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(default_fee__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = ServiceSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "material":
            queryset = Material.objects.filter(organization=request.organization.pk).order_by('name')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(default_fee__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = MaterialSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        case "request":
            queryset = Request.objects.filter(organization=request.organization.pk).order_by('requester_first_name')
            if search:
                queryset = queryset.filter(
                Q(requester_first_name__icontains=search) |
                Q(requester_last_name__icontains=search) |
                Q(requester_email__icontains=search) |
                Q(requester_city__icontains=search) |
                Q(requester_state__icontains=search) |
                Q(requester_zip__icontains=search) |
                Q(requester_address__icontains=search) |
                Q(requester_phone__icontains=search) |
                Q(description__icontains=search) |
                Q(availability__icontains=search) |
                Q(request_status__icontains=search) |
                Q(job__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = RequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "invoice":
            queryset = Invoice.objects.filter(customer__organization=request.organization.pk).order_by('date_issued')
            if search:
                queryset = queryset.filter(
                    Q(date_issued__icontains=search) |
                    Q(date_due__icontains=search) |
                    Q(status__icontains=search) |
                    Q(customer__first_name__icontains=search) |
                    Q(customer__last_name__icontains=search) |
                    Q(payment_link__icontains=search) |
                    Q(sales_tax_percent__icontains=search) |
                    Q(discount__discount_name__icontains=search) |
                    Q(discount__discount_percent__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = InvoiceSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "booking":
            from_date_string = request.query_params.get('from', '')
            to_date_string= request.query_params.get('to', '')
            if not from_date_string or not to_date_string:
                return Response({"message": "missing a starting date or ending date"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                from_date_time_object = timezone.make_aware(parse_datetime(from_date_string))
                to_date_time_object = timezone.make_aware(parse_datetime(to_date_string))
            except Exception:
                return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = Booking.objects.filter(organization=request.organization.pk).order_by('start_time')
            queryset = queryset.filter(
                    Q(start_time__gte=from_date_time_object) &
                    Q(end_time__lte=to_date_time_object)
            )
            serializer = BookingSerializer(queryset, many=True)

            raw_data = serializer.data
            job_data = []
            event_data = []
            for event in raw_data:
                event_entry = {
                    "id": event["id"],
                    "event_name": event["event_name"],
                    "start_time": event["start_time"],
                    "end_time": event["end_time"],
                    "job": event["job"]["id"],
                    "booking_type": event["booking_type"],
                    "status": event["status"],
                    "back_color": event["back_color"]
                }
                event_data.append(event_entry)
            for event in raw_data:
                temp_job = event["job"]
                job_entry = {
                    "data":
                {
                    "endDate": temp_job['endDate'],
                    "description": temp_job['description'],
                    "customerName": temp_job['customerName']
                }
                }
                job_data.append(job_entry)

            return Response({
                "event_data": event_data,
                "job_data": job_data,
            }, status=status.HTTP_200_OK)

        case "discount":
            queryset = Discount.objects.filter(organization=request.organization.pk).order_by('discount_name')
            if search:
                queryset = queryset.filter(
                    Q(discount_name__icontains=search) |
                    Q(discount_percent__icontains=search)
                )
            if exclude:
                queryset = queryset.exclude(id__in=exclude_ids) if exclude_ids else queryset.exclude(id__in=[])
            page = paginator.paginate_queryset(queryset, request)
            serializer = DiscountSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

def get_individual_data(request, object_id, object_type):
    match object_type:

        case "discount":
            try:
                query = Discount.objects.get(pk=object_id, organization=request.organization.pk)
            except Discount.DoesNotExist:
                return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DiscountSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "job_template":
            try:
                query = JobTemplate.objects.get(pk=object_id, organization=request.organization.pk)
            except JobTemplate.DoesNotExist:
                return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The job template does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobTemplateSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "contractor":
            try:
                query = Contractor.objects.get(pk=object_id, organization=request.organization.pk)
            except Contractor.DoesNotExist:
                return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The contractor does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ContractorSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "customer":
            try:
                query = Customer.objects.get(pk=object_id, organization=request.organization.pk)
            except Customer.DoesNotExist:
                return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "job":
            try:
                query = Job.objects.get(pk=object_id, organization=request.organization.pk)
            except Job.DoesNotExist:
                return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobSerializer(query)

            return Response({
                "data": serializer.to_representation(query),
                "services": serializer.services_representation(query),
                "materials": serializer.materials_representation(query),
                "contractors": serializer.contractors_representation(query)
                            }, status=status.HTTP_200_OK)
        case "service":
            try:
                query = Service.objects.get(pk=object_id, organization=request.organization.pk)
            except Service.DoesNotExist:
                return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The service does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ServiceSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "material":
            try:
                query = Material.objects.get(pk=object_id, organization=request.organization.pk)
            except Material.DoesNotExist:
                return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The material does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = MaterialSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case "request":
            try:
                query = Request.objects.get(pk=object_id, organization=request.organization.pk)
            except Request.DoesNotExist:
                return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The request does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = RequestSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "invoice":
            try:
                query = Invoice.objects.get(pk=object_id, customer__organization=request.organization.pk)
            except Invoice.DoesNotExist:
                return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The invoice does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = InvoiceSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case "booking":
            try:
                query = Booking.objects.get(pk=object_id, organization=request.organization.pk)
            except Booking.DoesNotExist:
                return Response({"message": "The booking does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if not query:
                return Response({"message": "The booking does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookingSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

def create_individual_data(request, object_type):
    data = request.data
    match object_type:
        case "discount":
            discount_data = {
                "discount_name": data.get("name"),
                "discount_percent": data.get("percent"),
                "organization": request.organization
            }
            data = discount_data
            serializer = DiscountSerializer(data=data)
        case "job_template":
            serializer = JobTemplateSerializer(data=data)
        case "contractor":
            contractor_data = {
                'first_name': data.get('firstName'),
                'last_name': data.get('lastName'),
                'email': data.get('email'),
                'phone': data.get('phone').replace("-",""),
                'organization': request.organization,
            }
            data = contractor_data
            serializer = ContractorSerializer(data=data)
        case "customer":
            customer_data = {
                "first_name": data.get("firstn"),
                "last_name": data.get("lastn"),
                "email": data.get("email"),
                "phone": data.get("phoneno"),
                "notes": data.get("notes"),
                "organization": request.organization,
            }
            data = customer_data
            serializer = CustomerSerializer(data=data)
        case "job":
            serializer = JobSerializer(data=data)
        case "service":
            if data.get('default_fee') == '' or data.get('default_fee') is None:
                default_fee = 0
            else:
                default_fee = data.get('default_fee')
            service_data = {
                "name": data.get('service_name'),
                "description": data.get('service_description'),
                "default_fee": default_fee,
                "organization": request.organization,
            }
            data = service_data
            serializer = ServiceSerializer(data=data)
        case "material":
            if data.get('default_cost') == '' or data.get('default_cost') is None:
                default_cost = 0
            else:
                default_cost = data.get('default_fee')

            material_data = {
                "name": data.get('material_name'),
                "description": data.get('description'),
                "default_cost": default_cost,
                "organization": request.organization,
            }
            data = material_data
            serializer = MaterialSerializer(data=data)
        case "request":
            serializer = RequestSerializer(data=data)
        case "invoice":
            serializer = InvoiceSerializer(data=data)
        case "booking":
            serializer = BookingSerializer(data=data)

        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    if serializer.is_valid():
        serializer.create(data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_individual_data(request, object_id, object_type):
    data = request.data
    match object_type:
        case "discount":
            discount_data = {
                "discount_name": data.get("name"),
                "discount_percent": data.get("percent")
            }
            data = discount_data
            query_object = Discount.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = DiscountSerializer(query_object, data=data)
        case "job_template":
            query_object = JobTemplate.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = JobTemplateSerializer(query_object, data=data)
        case "contractor":
            query_object = Contractor.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = ContractorSerializer(query_object, data=data)
        case "customer":
            customer_data = {
                "first_name": data.get("firstn"),
                "last_name": data.get("lastn"),
                "email": data.get("email"),
                "phone": data.get("phoneno"),
                "notes": data.get("notes"),
            }
            data = customer_data
            query_object = Customer.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = CustomerSerializer(query_object, data=data)
        case "job":
            customer_temp = Customer.objects.filter(organization=request.organization.pk, pk=data.get('customerID')).first()
            job_data = {
                "job_status": data.get("jobStatus"),
                "job_address": data.get("address"),
                "job_city": data.get("city"),
                "description": data.get("description"),
                "start_date": data.get("startDate"),
                "end_date": data.get("endDate"),
                "job_state": data.get("state"),
                "job_zip": data.get("zip"),
                "customer": customer_temp
            }
            data = job_data
            query_object = Job.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = JobSerializer(query_object, data=data)
        case "service":
            if data.get('default_fee') == '' or data.get('default_fee') is None:
                default_fee = 0
            else:
                default_fee = data.get('default_fee')
            service_data = {
                "name": data.get('service_name'),
                "description": data.get('service_description'),
                "default_fee": default_fee,
                "organization": request.organization,
            }
            data = service_data
            query_object = Service.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = ServiceSerializer(query_object, data=data)
        case "material":
            default_cost = data.get('default_cost')
            default_cost = float(default_cost) if default_cost else 0
            material_data = {
                "name": data.get('material_name'),
                "description": data.get('description'),
                "default_cost": default_cost,
            }
            data = material_data
            query_object = Material.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = MaterialSerializer(query_object, data=data)
        case "request":
            query_object = Request.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = RequestSerializer(query_object, data=data)
        case "invoice":
            query_object = Invoice.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = InvoiceSerializer(query_object, data=data)
        case "booking":
            query_object = Booking.objects.filter(organization=request.organization.pk, pk=object_id).first()
            serializer = BookingSerializer(query_object, data=data)
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    if serializer.is_valid():
        serializer.update(query_object, data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_object(request, object_id, object_type):
    match object_type:
        case "discount":
            query_object = Discount.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "job_template":
            query_object = JobTemplate.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "contractor":
            query_object = Contractor.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "customer":
            query_object = Customer.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "job":
            query_object = Job.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "service":
            query_object = Service.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "material":
            query_object = Material.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "request":
            query_object = Request.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "invoice":
            query_object = Invoice.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case "booking":
            query_object = Booking.objects.filter(organization=request.organization.pk, pk=object_id).first()
        case _:
            return Response(
                data={
                    "message": "Invalid model type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    try:
        query_object.delete()
        return Response({
            "message": object_type + " deleted successfully"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "message": "Error deleting " + object_type + ": " + str(e)
        }, status=status.HTTP_400_BAD_REQUEST)