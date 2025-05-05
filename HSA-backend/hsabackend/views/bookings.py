from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hsabackend.models.booking import Booking
from hsabackend.models.job import Job
from hsabackend.models.organization import Organization
from hsabackend.serializers.booking_serializer import BookingSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.response_helpers import get_table_data


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_booking_data(request):
    return get_table_data(request, "booking")

    # org = request.organization
    # from_date_string = request.query_params.get('from', '')
    # to_date_string= request.query_params.get('to', '')
    #
    # if not from_date_string or not to_date_string:
    #     return Response({"message": "missing a starting date or ending date"}, status=status.HTTP_400_BAD_REQUEST)
    #
    # try:
    #     from_date_time_object = timezone.make_aware(parse_datetime(from_date_string))
    #     to_date_time_object = timezone.make_aware(parse_datetime(to_date_string))
    # except Exception:
    #     return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
    #
    # bookings = Booking.objects.filter(organization=org.pk).filter(Q(start_time__gte=from_date_time_object) & Q(end_time__lte=to_date_time_object))
    #
    # serializer = BookingSerializer(bookings, many=True)
    #
    # jobs = []
    #
    # for event in serializer.data:
    #     job_id = event["job"]
    #
    #     try:
    #         job = Job.objects.get(pk=job_id, organization=org)
    #     except Job.DoesNotExist:
    #         return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     job_services = JobsServices.objects.filter(job=job.pk)
    #     job_materials = JobsMaterials.objects.filter(job=job.pk)
    #     job_contractors = job.contractors
    #
    #     job_services_data = []
    #     for service in job_services:
    #         job_services_data.append(service.json())
    #
    #     job_materials_data = []
    #     for material in job_materials:
    #         job_materials_data.append(material.json())
    #
    #     job_contractors_data = []
    #     for contractor in job_contractors:
    #         job_contractors_data.append(contractor.json())
    #
    #     job_data = {
    #         'data': job.json(),
    #         'services': job_services_data,
    #         'materials': job_materials_data,
    #         'contractors': job_contractors_data
    #     }
    #
    #     jobs.append(job_data)
    #
    #
    # res = {
    #     'event_data': serializer.data,
    #     'job_data': jobs
    # }

    # return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_event(request):
    org = Organization.objects.get(owning_user=request.user)
    job_id = request.data.get('jobID')

    try:
        start_time_string = request.data.get('startTime', '')
        end_time_string = request.data.get('endTime', '')
        start_time_object = timezone.make_aware(parse_datetime(start_time_string))
        end_time_object = timezone.make_aware(parse_datetime(end_time_string))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
    
    if start_time_object > end_time_object:
        return Response({"message": "Start must be before end"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        job_object = Job.objects.get(organization=org, pk=job_id)
    except Job.DoesNotExist:
        return Response({"errors": "Job not found"}, status=status.HTTP_400_BAD_REQUEST)

    # Prepare event data
    event_data = {
        'event_name': request.data.get('eventName', ''),
        'start_time': start_time_object,
        'end_time': end_time_object,
        'booking_type': request.data.get('bookingType', ''),
        'back_color': request.data.get('backColor', ''),
        'status': 'pending',
        'organization': org,
        'job': job_object,
        'job_id': job_id,
        'organization_id': org.pk,
    }

    # Create and validate event
    booking_serializer = BookingSerializer(data=event_data)

    if not booking_serializer.is_valid():
        return Response({"errors": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    booking_serializer.create(event_data)

    return Response({"message": "Event created successfully", "data": booking_serializer.data}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_event(request, booking_id):
    org = Organization.objects.get(owning_user=request.user)
    job_id = request.data.get('jobID')

    try:
        start_time_string = request.data.get('startTime', '')
        end_time_string = request.data.get('endTime', '')
        start_time_object = timezone.make_aware(parse_datetime(start_time_string))
        end_time_object = timezone.make_aware(parse_datetime(end_time_string))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
    
    if start_time_object > end_time_object:
        return Response({"message": "Start must be before end"}, status=status.HTTP_400_BAD_REQUEST)

    # Find the job model
    try:
        job_object = Job.objects.get(organization=org, pk=job_id)
    except Job.DoesNotExist:
        return Response({"errors": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Find the event model
    try:
        event_object = Booking.objects.get(organization=org, pk=booking_id)
    except Booking.DoesNotExist:
        return Response({"errors": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    # Prepare event data
    event_data = {
        'event_name': request.data.get('eventName', ''),
        'start_time': start_time_object,
        'end_time': end_time_object,
        'booking_type': request.data.get('bookingType', ''),
        'back_color': request.data.get('backColor', ''),
        'status': request.data.get('status'),
        'organization': org.pk,
        'job': job_object.pk
    }

    # Edit and validate event
    booking_serializer = BookingSerializer(event_object, data=event_data, partial=True)

    if not booking_serializer.is_valid():
        return Response({"errors": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    booking = booking_serializer.save()

    return Response({"message": "Event edited successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_event(request, booking_id):
    org = Organization.objects.get(owning_user=request.user)
    event_object = Booking.objects.filter(pk=booking_id, organization=org)

    if not event_object.exists():
        return Response({"message": "The event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    event_object[0].delete()
    return Response({"message": "Event deleted sucessfully"}, status=status.HTTP_200_OK)