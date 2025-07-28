
from django import forms
from django.core.exceptions import ValidationError

# Import models from other apps - ADJUST THESE APP NAMES TO MATCH YOUR PROJECT
from vehicleMaster.models import Vehicle  # Adjust app name
from routeMaster.models import Route  # Adjust app name  
from scheduleMaster.models import ScheduleMaster  # Adjust app name
from crewMaster.models import CrewMaster  # Adjust app name
from .models import Waybill

class WaybillForm(forms.ModelForm):
    class Meta:
        model = Waybill
        fields = ['vehicle', 'waybill_date', 'route', 'schedule', 'conductor', 'driver', 'status', 'remarks']
        widgets = {
            'waybill_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'vehicle': forms.Select(attrs={
                'class': 'form-control'
            }),
            'route': forms.Select(attrs={
                'class': 'form-control'
            }),
            'schedule': forms.Select(attrs={
                'class': 'form-control'
            }),
            'conductor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'driver': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any remarks or notes...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter conductors and drivers
        self.fields['conductor'].queryset = CrewMaster.objects.filter(
            role='Conductor', status='Active'
        )
        self.fields['driver'].queryset = CrewMaster.objects.filter(
            role='Driver', status='Active'
        )
        self.fields['schedule'].queryset = ScheduleMaster.objects.filter(status='Active')
    
    def clean(self):
        cleaned_data = super().clean()
        conductor = cleaned_data.get('conductor')
        driver = cleaned_data.get('driver')
        
        if conductor and driver and conductor == driver:
            raise ValidationError("Conductor and Driver must be different persons.")
        
        return cleaned_data

class WaybillSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Waybill Number, Vehicle Number, or Route',
            'id': 'search-input'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Waybill.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )