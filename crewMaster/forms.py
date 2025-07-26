from django import forms
from django.contrib.auth.hashers import make_password
from .models import CrewMaster

class CrewMasterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        help_text="Password will be securely hashed"
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        help_text="Re-enter the same password"
    )
    
    class Meta:
        model = CrewMaster
        fields = ['crew_id', 'crew_name', 'email', 'password', 'role', 'status']
        widgets = {
            'crew_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crew ID'
            }),
            'crew_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crew name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
    
    def save(self, commit=True):
        crew = super().save(commit=False)
        if self.cleaned_data['password']:
            crew.set_password(self.cleaned_data['password'])
        if commit:
            crew.save()
        return crew

class CrewMasterUpdateForm(forms.ModelForm):
    """Form for updating crew without password fields"""
    class Meta:
        model = CrewMaster
        fields = ['crew_id', 'crew_name', 'email', 'role', 'status']
        widgets = {
            'crew_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crew ID'
            }),
            'crew_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter crew name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class PasswordChangeForm(forms.Form):
    """Separate form for changing password"""
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data