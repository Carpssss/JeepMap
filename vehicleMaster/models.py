from django.db import models
from django.urls import reverse

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Bus', 'Bus'),
        ('Car', 'Car'),
        ('Truck', 'Truck'),
        ('Motorcycle', 'Motorcycle'),
        ('Van', 'Van'),
    ]
    
    vehicle_number = models.CharField(max_length=20, unique=True, verbose_name="Vehicle Number")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, verbose_name="Vehicle Type")
    vehicle_owner = models.CharField(max_length=100, verbose_name="Vehicle Owner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['vehicle_number']
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_type}"
    
    def get_absolute_url(self):
        return reverse('vehicle_detail', kwargs={'pk': self.pk})

# forms.py
from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type', 'vehicle_owner']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter vehicle number (e.g., NAB 1234)'
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'vehicle_owner': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter owner name'
            }),
        }
    
    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data['vehicle_number'].upper()
        return vehicle_number

class VehicleSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search Vehicle Number or Vehicle Type',
            'id': 'search-input'
        })
    )