from django import forms
from .models import ScheduleMaster

class ScheduleMasterForm(forms.ModelForm):
    class Meta:
        model = ScheduleMaster
        fields = ['schedule_name', 'trips', 'start_time', 'end_time', 'status', 'description']
        widgets = {
            'schedule_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter schedule name (e.g., General Schedule)'
            }),
            'trips': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of trips'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description for this schedule'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError({
                    'end_time': 'End time must be after start time.'
                })
        
        return cleaned_data