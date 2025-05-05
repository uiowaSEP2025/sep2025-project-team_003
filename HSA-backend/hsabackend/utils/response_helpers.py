from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from hsabackend.models.booking import Booking
from hsabackend.models.contractor import Contractor
from hsabackend.models.customer import Customer
from hsabackend.models.discount import Discount
from hsabackend.models.invoice import Invoice
from hsabackend.models.job import Job, JobsServices, JobsMaterials
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.material import Material
from hsabackend.models.request import Request
from hsabackend.models.service import Service
from hsabackend.serializers.booking_serializer import BookingSerializer
from hsabackend.serializers.contractor_serializer import ContractorSerializer, ContractorTableSerializer
from hsabackend.serializers.customer_serializer import CustomerSerializer, CustomerTableSerializer
from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.serializers.invoice_serializer import InvoiceSerializer, InvoiceTableSerializer
from hsabackend.serializers.job_serializer import JobSerializer, JobTableSerializer, JobBookingDataSerializer, \
    services_representation, materials_representation, contractors_representation
from hsabackend.serializers.job_service_serializer import JobServiceSerializer
from hsabackend.serializers.job_template_serializer import JobTemplateSerializer
from hsabackend.serializers.material_serializer import MaterialSerializer
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


def get_table_data(request, object_type, exclude=False, customer_id=None):
    search = request.query_params.get('search', '')
    paginator = CustomPagination()

    if exclude:
        excluded_ids_str = request.GET.getlist('excludeIDs', [])
        exclude_ids = [int(id) for id in excluded_ids_str]

    match object_type:
        case "customer_quotes":
            queryset = Job.objects.filter(organization=request.organization.pk, job_status='completed', customer=customer_id).order_by('start_date')
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
                    Q(default_cost__icontains=search)
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
            serializer = InvoiceTableSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        case "booking":
            contractor_id = request.query_params.get('contractor', '')
            from_date_string = request.query_params.get('from', '')
            to_date_string= request.query_params.get('to', '')
            if not from_date_string or not to_date_string:
                return Response({"message": "missing a starting date or ending date"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                from_date_time_object = timezone.make_aware(parse_datetime(from_date_string))
                to_date_time_object = timezone.make_aware(parse_datetime(to_date_string))
            except Exception:
                return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
            if contractor_id == 'undefined':
                queryset = Booking.objects.filter(organization=request.organization.pk).order_by('start_time')
            else:
                jobs_temp = Job.objects.filter(organization=request.organization.pk, contractors__id=contractor_id).order_by('start_date')
                jobs = []
                for job in jobs_temp:
                    jobs.append(job.id)
                queryset = Booking.objects.filter(organization=request.organization.pk, job__id__in=jobs).order_by('start_time')
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
                temp_job = Job.objects.get(pk=event["job"]["id"], organization=request.organization.pk)
                temp_serializer = JobBookingDataSerializer(temp_job)
                job_data.append(temp_serializer.data)

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
                "services": services_representation(query),
                "materials": materials_representation(query),
                "contractors": contractors_representation(query)
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
            try:
                contractor_data = {
                    'first_name': data.get('firstName'),
                    'last_name': data.get('lastName'),
                    'email': data.get('email'),
                    'phone': data.get('phone').replace("-",""),
                    'organization': request.organization,
                }
                data = contractor_data
                serializer = ContractorSerializer(data=data)
            except AttributeError:
                return Response({"message": "unknown error"},status=status.HTTP_400_BAD_REQUEST)
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
            contractor_ids = []
            for contractor in data.get('contractors'):
                contractor_ids.append(contractor.get('id'))
            material_ids = []
            for material in data.get('materials'):
                material_ids.append(material.get('id'))
            contractors_temp = Contractor.objects.filter(organization=request.organization.pk, pk__in=contractor_ids).all()
            materials_temp = Material.objects.filter(organization=request.organization.pk, pk__in=material_ids).all()
            job_data = {
                "job_status": data.get("jobStatus"),
                "job_address": data.get("address"),
                "job_city": data.get("city"),
                "description": data.get("description"),
                "start_date": data.get("startDate"),
                "end_date": data.get("endDate"),
                "job_state": data.get("state"),
                "job_zip": data.get("zip"),
            }
            serializer = JobSerializer(data=data)
        case "service":
            try:
                default_fee = float(data.get('default_fee'))
            except ValueError:
                default_fee = 0.00
            service_data = {
                "name": data.get('service_name'),
                "description": data.get('service_description'),
                "default_fee": default_fee,
                "organization": request.organization,
            }
            data = service_data
            serializer = ServiceSerializer(data=data)
        case "material":
            try:
                default_cost = float(data.get('default_cost'))
            except ValueError:
                default_cost = 0.00
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
            customer = Customer.objects.get(organization=request.organization.pk, pk=data.get('customerID'))
            invoice_data = {
                "customer": customer,
                "date_issued": data.get("dateIssued"),
                "date_due": data.get("dateDue"),
                "sales_tax_percent": data.get("taxPercent"),
                "payment_link": request.organization.default_payment_link,
            }
            data = invoice_data
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
        result = serializer.create(data)
        if object_type == "invoice":
            jobs_list = request.data.get("quoteIDs")
            for job in jobs_list:
                job_object = Job.objects.get(organization=request.organization.pk, pk=job)
                job_object.invoice = result
                job_object.save()
            response = InvoiceSerializer(result).data
        else:
            response = serializer.data
        return Response(
            response, status=status.HTTP_201_CREATED)
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
            query_object = Discount.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = DiscountSerializer(query_object, data=data)
        case "job_template":
            query_object = JobTemplate.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = JobTemplateSerializer(query_object, data=data)
        case "contractor":
            contractor_data = {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "email": data.get("email"),
                "phone": data.get("phone").replace("-",""),
                "notes": data.get("notes"),
            }
            data = contractor_data
            query_object = Contractor.objects.get(organization=request.organization.pk, pk=object_id)
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
            query_object = Customer.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = CustomerSerializer(query_object, data=data)
        case "job":
            material_ids = []
            material_list = []
            for material in data.get('materials'):
                material_ids.append(material.get('id'))
                material_list.append(material)
            service_ids = []
            service_list = []
            for service in data.get('services'):
                service_ids.append(service.get('id'))
                service_list.append(service)
            customer_temp = Customer.objects.get(organization=request.organization.pk, pk=data.get('customerID'))
            materials_temp = Material.objects.filter(organization=request.organization.pk, pk__in=material_ids).all()
            services_temp = Service.objects.filter(organization=request.organization.pk, pk__in=service_ids).all()
            contractors_temp = Contractor.objects.filter(organization=request.organization.pk, pk__in=data.get('contractors')).all()
            job_data = {
                "job_status": data.get("jobStatus"),
                "job_address": data.get("address"),
                "job_city": data.get("city"),
                "description": data.get("description"),
                "start_date": data.get("startDate"),
                "end_date": data.get("endDate"),
                "job_state": data.get("state"),
                "job_zip": data.get("zip"),
                "customer": customer_temp,
                "materials": materials_temp,
                "services": services_temp,
                "contractors": contractors_temp,
            }
            data = job_data
            query_object = Job.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = JobSerializer(query_object, data=data)
        case "service":
            try:
                default_fee = float(data.get('default_fee'))
            except* ValueError:
                default_fee = 0.00
            except* TypeError:
                default_fee = 0.00
            service_data = {
                "name": data.get('service_name'),
                "description": data.get('service_description'),
                "default_fee": default_fee,
                "organization": request.organization,
            }
            data = service_data
            query_object = Service.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = ServiceSerializer(query_object, data=data)
        case "material":
            try:
                default_cost = float(data.get('default_cost'))
            except* ValueError:
                default_cost = 0.00
            except* TypeError:
                default_cost = 0.00
            material_data = {
                "name": data.get('material_name'),
                "description": data.get('description'),
                "default_cost": default_cost,
            }
            data = material_data
            query_object = Material.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = MaterialSerializer(query_object, data=data)
        case "request":
            query_object = Request.objects.get(organization=request.organization.pk, pk=object_id)
            serializer = RequestSerializer(query_object, data=data)
        case "invoice":
            query_object = Invoice.objects.get(pk=object_id)
            customer_object = Customer.objects.get(pk=data.get('customerId'))
            customer_serializer = CustomerSerializer(customer_object).data
            invoice_data = {
                "date_issued": data.get("dateIssued"),
                "date_due": data.get("dateDue"),
                "sales_tax_percent": data.get("taxPercent"),
                "payment_link": data.get("paymentLink"),
                "customer": customer_object,
            }
            data = invoice_data
            serializer = InvoiceSerializer(query_object, data=data)
        case "booking":
            query_object = Booking.objects.get(organization=request.organization.pk, pk=object_id)
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
        if object_type == "job":
            update_job_joins(query_object, service_list, material_list)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobsMaterialSerializer:
    pass


def update_job_joins(job, services, materials):
    org_id = job.organization.pk

    for service in services:
        temp_service = Service.objects.get(organization=org_id, pk=service.get('id'))
        job_service = JobsServices.objects.get(job=job, service=temp_service)
        job_service.fee = service.get('fee')
        job_service.save()
    for material in materials:
        temp_material = Material.objects.get(organization=org_id, pk=material.get('id'))
        job_material = JobsMaterials.objects.get(job=job, material=temp_material)
        job_material.quantity = material.get('unitsUsed')
        job_material.unit_cost = material.get('pricePerUnit')
        job_material.save()
    return


def delete_object(request, object_id, object_type):
    match object_type:
        case "discount":
            try:
                query_object = Discount.objects.get(organization=request.organization.pk, pk=object_id)
            except Discount.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "job_template":
            try:
                query_object = JobTemplate.objects.get(organization=request.organization.pk, pk=object_id)
            except JobTemplate.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "contractor":
            try:
                query_object = Contractor.objects.get(organization=request.organization.pk, pk=object_id)
            except Contractor.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "customer":
            try:
                query_object = Customer.objects.get(organization=request.organization.pk, pk=object_id)
            except Customer.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "job":
            try:
                query_object = Job.objects.get(organization=request.organization.pk, pk=object_id)
            except Job.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "service":
            try:
                query_object = Service.objects.get(organization=request.organization.pk, pk=object_id)
            except Service.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "material":
            try:
                query_object = Material.objects.get(organization=request.organization.pk, pk=object_id)
            except Material.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "request":
            try:
                query_object = Request.objects.get(organization=request.organization.pk, pk=object_id)
            except Request.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "invoice":
            try:
                query_object = Invoice.objects.get(pk=object_id)
            except Invoice.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        case "booking":
            try:
                query_object = Booking.objects.get(organization=request.organization.pk, pk=object_id)
            except Booking.DoesNotExist:
                return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
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