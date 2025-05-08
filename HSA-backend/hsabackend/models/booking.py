from django.db import models

from hsabackend.models.job import Job
from hsabackend.models.organization import Organization


class Booking(models.Model):
    """A Reservation to go out to a job site for giving out a quote or working on a job"""
    type_choices = [
        ('job', 'job'),
        ('quote', 'quote'),
    ]

    status_choices = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('cancelled', 'cancelled'),
    ]

    event_name = models.CharField(max_length=50, default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    booking_type = models.CharField(max_length=50, choices=type_choices, default="job")
    status = models.CharField(max_length=50, choices=status_choices, default="pending")
    back_color = models.CharField(max_length=50, default='#6aa84f', blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # DO NOT SET THIS in the backend, only for celery worker!!!!
    notified = models.BooleanField(default=False, blank=True) # have the contractors and the custmer been notified? 
    

    @property
    def booking_date(self):
        """Returns the date portion of start_time"""
        return self.start_time.date()

    @property
    def duration(self):
        """Returns the duration in minutes between start_time and end_time"""
        time_difference = self.end_time - self.start_time
        return int(time_difference.total_seconds() / 60)
    
    @property
    def full_display_address(self):
        """Returns the displayable address"""
        return f"{self.job.requestor_address}, {self.job.requestor_city}, {self.job.requestor_state}, {self.job.requestor_zip}"


    def __str__(self):
        return (f"<Booking Details:"
                f" id: {self.pk},"
                f" event_name: {self.event_name},"
                f" booking_date: {self.booking_date},"
                f" start_time: {self.start_time},"
                f" end_time: {self.end_time},"
                f" status: {self.status},"
                f" booking_type: {self.booking_type},"
                f" job: {self.job}, "
                f" duration: {self.duration}"
                f" organization: {self.organization}")