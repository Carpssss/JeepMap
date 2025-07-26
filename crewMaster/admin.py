from django.contrib import admin
from .models import CrewMaster

@admin.register(CrewMaster)
class CrewMasterAdmin(admin.ModelAdmin):
    list_display = ['crew_id', 'crew_name', 'email', 'role', 'status', 'created_at']
    list_filter = ['role', 'status', 'created_at']
    search_fields = ['crew_id', 'crew_name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'qr_code']
    ordering = ['crew_id']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Generate QR code if it doesn't exist
        if not obj.qr_code:
            obj.generate_qr_code()
            obj.save(update_fields=['qr_code'])
