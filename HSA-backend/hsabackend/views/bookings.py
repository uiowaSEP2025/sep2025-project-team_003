from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from hsabackend.models.organization import Organization
from hsabackend.models.booking import Booking
from hsabackend.models.job import Job
from hsabackend.serializers.booking_serializer import BookingSerializer
from django.db.models import Q
from django.core.exceptions import ValidationError
from hsabackend.utils.auth_wrapper import check_authenticated_and_onboarded

@api_view(["GET"])
@check_authenticated_and_onboarded()
def get_booking_data(request):
    org = request.org
    fromDateString = request.query_params.get('from', '')
    toDateString= request.query_params.get('to', '')

    if not fromDateString or not toDateString:
        return Response({"message": "missing a starting date or ending date"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        fromDateTimeObject = timezone.make_aware(parse_datetime(fromDateString))
        toDateTimeObject = timezone.make_aware(parse_datetime(toDateString))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
    
    bookings = Booking.objects.filter(organization=org.pk).filter(Q(start_time__gte=fromDateTimeObject) & Q(end_time__lte=toDateTimeObject))
    count = Booking.objects.filter(organization=org.pk).filter(Q(start_time__lte=fromDateTimeObject) & Q(end_time__gte=toDateTimeObject)).count()

    serializer = BookingSerializer(bookings, many=True)

    res = {
        'data': serializer.data,
        'totalCount': count
    }    
    print(serializer.data)
    return Response(res, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_event(request):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user)
    job_id = request.data.get('jobID')

    try:
        startTimeString = request.data.get('startTime', '')
        endTimeString = request.data.get('endTime', '')
        startTimeObject = timezone.make_aware(parse_datetime(startTimeString))
        endTimeObject = timezone.make_aware(parse_datetime(endTimeString))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Find job model
    try:
        job_object = Job.objects.get(organization=org, pk=job_id)
    except Job.DoesNotExist:
        return Response({"errors": "Job not found"}, status=status.HTTP_400_BAD_REQUEST)

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

    booking = booking_serializer.save()

    return Response({"message": "Event created successfully"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def edit_event(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user)
    job_id = request.data.get('jobID')

    try:
        startTimeString = request.data.get('startTime', '')
        endTimeString = request.data.get('endTime', '')
        startTimeObject = timezone.make_aware(parse_datetime(startTimeString))
        endTimeObject = timezone.make_aware(parse_datetime(endTimeString))
    except Exception:
        return Response({"message": "Cannot parse date time"}, status=status.HTTP_400_BAD_REQUEST)
    
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

    print(event_data)

    # Edit and validate event
    booking_serializer = BookingSerializer(event_object, data=event_data, partial=True)

    if not booking_serializer.is_valid():
        return Response({"errors": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    booking = booking_serializer.save()

    return Response({"message": "Event edited successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def delete_event(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    org = Organization.objects.get(owning_User=request.user)
    event_object = Booking.objects.filter(pk=id, organization=org)

    if not event_object.exists():
        return Response({"message": "The event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    event_object[0].delete()
    return Response({"message": "Event deleted sucessfully"}, status=status.HTTP_200_OK)