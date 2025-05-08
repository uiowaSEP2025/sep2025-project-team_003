from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from io import BytesIO
from ics import Calendar, Event
from django.http import FileResponse
from django.utils import timezone
from hsabackend.models.organization import Organization
from hsabackend.models.booking import Booking
from hsabackend.models.job import Job
from hsabackend.models.job_service import JobService
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job_contractor import JobContractor
from hsabackend.serializers.booking_serializer import BookingSerializer
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded
from hsabackend.utils.api_validators import parse_and_return_int

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_ical_for_bookings(request): 
    org = request.org
    fromDateString = request.query_params.get('from', '')
    toDateString = request.query_params.get('to', '')
    contractor_id = request.query_params.get('contractor', '')

    if not fromDateString or not toDateString:
        return Response({"message": "missing a starting date or ending date"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        fromDateTimeObject = timezone.make_aware(parse_datetime(fromDateString))
        toDateTimeObject = timezone.make_aware(parse_datetime(toDateString))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)

    contractor_id = parse_and_return_int(contractor_id)

    if not contractor_id:
        return Response({"message": "Contractor id must be int"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(
        organization=org.pk,
        job__jobcontractor__contractor=contractor_id,
        start_time__gte=fromDateTimeObject,
        end_time__lte=toDateTimeObject
    ).select_related('job').distinct()

    c = Calendar()
    for booking in bookings:
        e = Event()
        e.name = booking.event_name
        e.begin = booking.start_time
        e.end = booking.end_time
        e.description = booking.job.description
        e.location = booking.full_display_address
        c.events.add(e)
    
    ical_file = BytesIO()
    ical_file.write(str(c).encode('utf-8'))
    ical_file.seek(0)

    return FileResponse(ical_file, as_attachment=True, filename="bookings.ics", content_type='text/calendar')


@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_booking_data(request):
    org = request.org
    fromDateString = request.query_params.get('from', '')
    toDateString = request.query_params.get('to', '')
    contractor_id = request.query_params.get('contractor', '')

    if not fromDateString or not toDateString:
        return Response({"message": "missing a starting date or ending date"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        fromDateTimeObject = timezone.make_aware(parse_datetime(fromDateString))
        toDateTimeObject = timezone.make_aware(parse_datetime(toDateString))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)

    contractor_id = parse_and_return_int(contractor_id)

    if not contractor_id:
        return Response({"message": "Contractor id must be int"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(
        organization=org.pk,
        job__jobcontractor__contractor=contractor_id,
        start_time__gte=fromDateTimeObject,
        end_time__lte=toDateTimeObject
    ).distinct()

    serializer = BookingSerializer(bookings, many=True)

    jobs = []

    for event in serializer.data:
        job_id = event["job"]

        try:
            job = Job.objects.get(pk=job_id, organization=org)
        except Job.DoesNotExist:
            return Response({"message": "The job does not exist"}, status=status.HTTP_404_NOT_FOUND)

        job_services = JobService.objects.filter(job=job.pk)
        job_materials = JobMaterial.objects.filter(job=job.pk)
        job_contractors = JobContractor.objects.filter(job=job.pk)

        job_services_data = []
        for service in job_services:
            job_services_data.append(service.json())

        job_materials_data = []
        for material in job_materials:
            job_materials_data.append(material.json())

        job_contractors_data = []
        for contractor in job_contractors:
            job_contractors_data.append(contractor.json())

        job_data = {
            'data': job.json(),
            'services': job_services_data,
            'materials': job_materials_data,
            'contractors': job_contractors_data
        }

        jobs.append(job_data)

    res = {
        'event_data': serializer.data,
        'job_data': jobs
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(["POST"])
@check_authenticated_and_onboarded()
def create_event(request):
    org = Organization.objects.get(owning_User=request.user)
    job_id = request.data.get('jobID')

    try:
        startTimeString = request.data.get('startTime', '')
        endTimeString = request.data.get('endTime', '')
        startTimeObject = timezone.make_aware(parse_datetime(startTimeString))
        endTimeObject = timezone.make_aware(parse_datetime(endTimeString))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)

    if startTimeObject > endTimeObject:
        return Response({"message": "Start must be before end"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        job_object = Job.objects.get(organization=org, pk=job_id)
    except Job.DoesNotExist:
        return Response({"errors": "Job not found"}, status=status.HTTP_400_BAD_REQUEST)

    if job_object.job_status == "completed":
        return Response({"message": "Job can't have status completed"}, status=status.HTTP_400_BAD_REQUEST)
    # Prepare event data
    event_data = {
        'event_name': request.data.get('eventName', ''),
        'start_time': startTimeObject,
        'end_time': endTimeObject,
        'booking_type': request.data.get('bookingType', ''),
        'back_color': request.data.get('backColor', ''),
        'status': 'pending',
        'organization': org.pk,
        'job': job_object.pk
    }

    # Create and validate event
    booking_serializer = BookingSerializer(data=event_data)

    if not booking_serializer.is_valid():
        return Response({"errors": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    booking_serializer.save()

    return Response({"message": "Event created successfully", "data": booking_serializer.data}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@check_authenticated_and_onboarded()
def edit_event(request, id):
    org = Organization.objects.get(owning_User=request.user)
    job_id = request.data.get('jobID')
    try:
        startTimeString = request.data.get('startTime', '')
        endTimeString = request.data.get('endTime', '')
        startTimeObject = timezone.make_aware(parse_datetime(startTimeString))
        endTimeObject = timezone.make_aware(parse_datetime(endTimeString))
    
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)

    if startTimeObject > endTimeObject:
        return Response({"message": "Start must be before end"}, status=status.HTTP_400_BAD_REQUEST)

    # Find job model
    try:
        job_object = Job.objects.get(organization=org, pk=job_id)
    except Job.DoesNotExist:
        return Response({"errors": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    # Find event model
    try:
        event_object = Booking.objects.get(organization=org, pk=id)
    except Booking.DoesNotExist:
        return Response({"errors": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    # Prepare event data
    event_data = {
        'event_name': request.data.get('eventName', ''),
        'start_time': startTimeObject,
        'end_time': endTimeObject,
        'booking_type': request.data.get('bookingType', ''),
        'back_color': request.data.get('backColor', ''),
        'status': request.data.get('status'),
        'organization': org.pk,
        'job': job_object.pk
    }

    # Edit and validate event
    booking_serializer = BookingSerializer(
        event_object, data=event_data, partial=True)

    if not booking_serializer.is_valid():
        return Response({"errors": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    booking_serializer.save()

    return Response({"message": "Event edited successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@check_authenticated_and_onboarded()
def delete_event(request, id):
    org = request.org
    event_object = Booking.objects.filter(pk=id, organization=org)

    if not event_object.exists():
        return Response({"message": "The event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    event_object[0].delete()
    return Response({"message": "Event deleted sucessfully"}, status=status.HTTP_200_OK)
