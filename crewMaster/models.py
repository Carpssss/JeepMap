from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File
import os

class CrewMaster(models.Model):
    ROLE_CHOICES = [
        ('Conductor', 'Conductor'),
        ('Driver', 'Driver'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    crew_id = models.CharField(max_length=50, unique=True, verbose_name="Crew ID")
    crew_name = models.CharField(max_length=100, verbose_name="Crew Name")
    email = models.EmailField(unique=True, verbose_name="Email")  # Added email field
    password = models.CharField(max_length=128, verbose_name="Password")  # Hashed password
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Role")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active', verbose_name="Status")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name="QR Code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'crew_master'
        verbose_name = 'Crew Master'
        verbose_name_plural = 'Crew Masters'
        ordering = ['crew_id']
    
    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)
    
    def generate_qr_code(self):
        """Generate QR code containing crew member's email"""
        if self.email:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            # QR code data - you can customize this as needed
            qr_data = {
                'email': self.email,
                'crew_id': self.crew_id,
                'crew_name': self.crew_name,
                'role': self.role
            }
            
            # For simple email QR code, just use email
            qr.add_data(self.email)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save to BytesIO
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Save to model
            filename = f'qr_code_{self.crew_id}.png'
            self.qr_code.save(filename, File(buffer), save=False)
            buffer.close()
    
    def save(self, *args, **kwargs):
        # Generate QR code if it doesn't exist or email changed
        if not self.qr_code or self.pk is None:
            super().save(*args, **kwargs)  # Save first to get pk
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])
        else:
            super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('crew_master:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f"{self.crew_id} - {self.crew_name}"