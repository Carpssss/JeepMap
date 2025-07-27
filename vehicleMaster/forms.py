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