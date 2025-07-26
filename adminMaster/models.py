from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class AdminMaster(models.Model):
    ROLE_CHOICES = [
        ('Bookkeeper', 'Bookkeeper'),
        ('Operations', 'Operations'),
        ('Manager', 'Manager'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    admin_id = models.CharField(max_length=50, unique=True)
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.admin_id} - {self.admin_name}"