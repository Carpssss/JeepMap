from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date

# Import models from other apps - ADJUST THESE APP NAMES TO MATCH YOUR PROJECT
from vehicleMaster.models import Vehicle  # Adjust app name
from routeMaster.models import Route  # Adjust app name  
from scheduleMaster.models import ScheduleMaster  # Adjust app name
from crewMaster.models import CrewMaster  # Adjust app name

class Waybill(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    waybill_number = models.CharField(max_length=20, unique=True, verbose_name="Waybill Number")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Vehicle")
    waybill_date = models.DateField(default=date.today, verbose_name="Waybill Date")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Route")
    schedule = models.ForeignKey(ScheduleMaster, on_delete=models.CASCADE, verbose_name="Schedule")
    conductor = models.ForeignKey(CrewMaster, on_delete=models.CASCADE, related_name='conductor_waybills', 
                                limit_choices_to={'role': 'Conductor', 'status': 'Active'}, verbose_name="Conductor")
    driver = models.ForeignKey(CrewMaster, on_delete=models.CASCADE, related_name='driver_waybills',
                             limit_choices_to={'role': 'Driver', 'status': 'Active'}, verbose_name="Driver")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', verbose_name="Status")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'waybill_master'
        verbose_name = 'Waybill'
        verbose_name_plural = 'Waybills'
        ordering = ['-waybill_date', '-created_at']
    
    def clean(self):
        # Ensure conductor and driver are different
        if hasattr(self, 'conductor') and hasattr(self, 'driver'):
            if self.conductor == self.driver:
                raise ValidationError("Conductor and Driver must be different persons.")
    
    def save(self, *args, **kwargs):
        if not self.waybill_number:
            # Auto-generate waybill number
            today = date.today()
            prefix = f"WB{today.strftime('%Y%m%d')}"
            last_waybill = Waybill.objects.filter(
                waybill_number__startswith=prefix
            ).order_by('-waybill_number').first()
            
            if last_waybill:
                try:
                    last_num = int(last_waybill.waybill_number[-3:])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            
            self.waybill_number = f"{prefix}{new_num:03d}"
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('waybill:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f"{self.waybill_number} - {self.vehicle.vehicle_number}"


class WaybillDetails(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Digital', 'Digital'),
        ('Mixed', 'Mixed'),
    ]
    
    waybill = models.OneToOneField(Waybill, on_delete=models.CASCADE, related_name='details', verbose_name="Waybill")
    
    # Amount Details & Payment Method
    actual_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Actual Amount")
    etim_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="ETIM Amount")
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Expenses")
    penalty_excess_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Penalty/Excess Amount")
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Sales")
    
    # Payment Method Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash', verbose_name="Payment Method")
    passenger_count = models.IntegerField(default=0, verbose_name="Passenger Count")
    collection = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Collection")
    payment_penalty_excess = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Payment Penalty/Excess Amount")
    payment_total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Payment Total Sales")
    
    # Totals
    total_cash_collection = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Cash Collection")
    completion_date = models.DateField(blank=True, null=True, verbose_name="Completion Date")
    
    # Additional fields
    fuel_consumption = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Fuel Consumption (Liters)")
    toll_fees = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Toll Fees")
    parking_fees = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Parking Fees")
    other_expenses = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Other Expenses")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'waybill_details'
        verbose_name = 'Waybill Detail'
        verbose_name_plural = 'Waybill Details'
    
    def save(self, *args, **kwargs):
        # Auto-calculate totals
        self.total_sales = self.actual_amount + self.penalty_excess_amount - self.expenses
        self.payment_total_sales = self.collection + self.payment_penalty_excess
        self.total_cash_collection = self.collection
        
        # Calculate total expenses
        self.expenses = self.fuel_consumption + self.toll_fees + self.parking_fees + self.other_expenses
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Details for {self.waybill.waybill_number}"


class WaybillTrip(models.Model):
    DIRECTION_CHOICES = [
        ('North-South', 'North-South'),
        ('South-North', 'South-North'),
    ]
    
    waybill = models.ForeignKey(Waybill, on_delete=models.CASCADE, related_name='trips', verbose_name="Waybill")
    trip_number = models.IntegerField(verbose_name="Trip Number")
    route_name = models.CharField(max_length=100, verbose_name="Route Name")
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES, verbose_name="Direction")
    passenger_count = models.IntegerField(default=0, verbose_name="Passenger Count")
    collection = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Collection")
    departure_time = models.TimeField(blank=True, null=True, verbose_name="Departure Time")
    arrival_time = models.TimeField(blank=True, null=True, verbose_name="Arrival Time")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'waybill_trips'
        verbose_name = 'Waybill Trip'
        verbose_name_plural = 'Waybill Trips'
        ordering = ['trip_number']
        unique_together = ['waybill', 'trip_number']
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.waybill.waybill_number}"