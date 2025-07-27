from django import forms
from .models import AdminMaster

class AdminMasterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter a secure password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Confirm your password"
    )
    
    class Meta:
        model = AdminMaster
        fields = ['admin_id', 'admin_name','admin_email', 'password', 'role', 'status']
        widgets = {
            'admin_id': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_name': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_email': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If updating, make password optional
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
            self.fields['password'].help_text = "Leave blank to keep current password"
            self.fields['confirm_password'].help_text = "Leave blank to keep current password"
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # If password is provided, validate confirmation
        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords don't match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        admin = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            from django.contrib.auth.hashers import make_password
            admin.password = make_password(password)  # Hash the password before saving

        if commit:
            admin.save()
        return admin

