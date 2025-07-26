from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class ScheduleMaster(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    schedule_name = models.CharField(max_length=100, verbose_name="Schedule Name")
    trips = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name="Number of Trips",
        help_text="Total number of trips for this schedule"
    )
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active', verbose_name="Status")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'schedule_master'
        verbose_name = 'Schedule Master'
        verbose_name_plural = 'Schedule Masters'
        ordering = ['schedule_name', 'start_time']
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError({
                    'end_time': 'End time must be after start time.'
                })
    
    @property
    def duration(self):
        """Calculate duration between start and end time"""
        if self.start_time and self.end_time:
            from datetime import datetime, timedelta
            start = datetime.combine(datetime.today(), self.start_time)
            end = datetime.combine(datetime.today(), self.end_time)
            
            # Handle next day scenario
            if end < start:
                end += timedelta(days=1)
            
            duration = end - start
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours}h {minutes}m"
        return "N/A"
    
    def __str__(self):
        return f"{self.schedule_name} ({self.trips} trips)"