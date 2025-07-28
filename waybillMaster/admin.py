from django.contrib import admin
from django.utils.html import format_html
from .models import Waybill

@admin.register(Waybill)
class WaybillAdmin(admin.ModelAdmin):
    list_display = [
        'waybill_number', 
        'vehicle_display', 
        'waybill_date', 
        'route_display', 
        'schedule_display',
        'conductor_display', 
        'driver_display', 
        'status_display',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'waybill_date',
        'vehicle__vehicle_type',
        'route',
        'schedule',
        'created_at'
    ]
    
    search_fields = [
        'waybill_number',
        'vehicle__vehicle_number',
        'route__route_name',
        'conductor__crew_name',
        'driver__crew_name'
    ]
    
    readonly_fields = ['waybill_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Waybill Information', {
            'fields': ('waybill_number', 'waybill_date', 'status', 'remarks')
        }),
        ('Vehicle & Route', {
            'fields': ('vehicle', 'route', 'schedule')
        }),
        ('Crew Assignment', {
            'fields': ('conductor', 'driver')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'waybill_date'
    ordering = ['-waybill_date', '-created_at']
    
    def vehicle_display(self, obj):
        return f"{obj.vehicle.vehicle_number} ({obj.vehicle.vehicle_type})"
    vehicle_display.short_description = 'Vehicle'
    vehicle_display.admin_order_field = 'vehicle__vehicle_number'
    
    def route_display(self, obj):
        return obj.route.route_name
    route_display.short_description = 'Route'
    route_display.admin_order_field = 'route__route_name'
    
    def schedule_display(self, obj):
        return f"{obj.schedule.schedule_name} ({obj.schedule.trips} trips)"
    schedule_display.short_description = 'Schedule'
    schedule_display.admin_order_field = 'schedule__schedule_name'
    
    def conductor_display(self, obj):
        return f"{obj.conductor.crew_name} ({obj.conductor.crew_id})"
    conductor_display.short_description = 'Conductor'
    conductor_display.admin_order_field = 'conductor__crew_name'
    
    def driver_display(self, obj):
        return f"{obj.driver.crew_name} ({obj.driver.crew_id})"
    driver_display.short_description = 'Driver'
    driver_display.admin_order_field = 'driver__crew_name'
    
    def status_display(self, obj):
        colors = {
            'Active': 'green',
            'Completed': 'blue',
            'Cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'vehicle', 'route', 'schedule', 'conductor', 'driver'
        )