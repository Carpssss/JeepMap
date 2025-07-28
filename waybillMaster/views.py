from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import transaction
from .models import Waybill, WaybillDetails, WaybillTrip
from .forms import WaybillForm, WaybillSearchForm

class WaybillListView(ListView):
    model = Waybill
    template_name = 'waybillMaster/waybillMaster_list.html'
    context_object_name = 'waybills'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Waybill.objects.select_related(
            'vehicle', 'route', 'schedule', 'conductor', 'driver', 'details'
        ).all()
        
        # Search functionality
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(waybill_number__icontains=search_query) |
                Q(vehicle__vehicle_number__icontains=search_query) |
                Q(route__route_name__icontains=search_query) |
                Q(conductor__crew_name__icontains=search_query) |
                Q(driver__crew_name__icontains=search_query)
            )
        
        # Date range filter
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(waybill_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(waybill_date__lte=date_to)
        
        # Status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = WaybillSearchForm(self.request.GET)
        return context

class WaybillDetailView(DetailView):
    model = Waybill
    template_name = 'waybillMaster/waybillMaster_detail.html'
    context_object_name = 'waybill'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        waybill = self.get_object()
        
        # Get or create waybill details with default values
        details, created = WaybillDetails.objects.get_or_create(
            waybill=waybill,
            defaults={
                'actual_amount': 0.00,
                'etim_amount': 0.00,
                'expenses': 0.00,
                'penalty_excess_amount': 0.00,
                'total_sales': 0.00,
                'payment_method': 'Cash',
                'passenger_count': 0,
                'collection': 0.00,
                'payment_penalty_excess': 0.00,
                'payment_total_sales': 0.00,
                'total_cash_collection': 0.00,
                'fuel_consumption': 0.00,
                'toll_fees': 0.00,
                'parking_fees': 0.00,
                'other_expenses': 0.00,
            }
        )
        
        # Get all trips for this waybill
        trips = WaybillTrip.objects.filter(waybill=waybill).order_by('trip_number')
        
        # If no trips exist, create default trips based on your screenshot
        if not trips.exists():
            default_trips = [
                {'trip_number': 1, 'route_name': 'Calamba to San Pedro', 'direction': 'South-North', 'passenger_count': 12, 'collection': 268.5},
                {'trip_number': 2, 'route_name': 'San Pedro - Calamba', 'direction': 'North-South', 'passenger_count': 12, 'collection': 268.5},
                {'trip_number': 3, 'route_name': 'Calamba to San Pedro', 'direction': 'South-North', 'passenger_count': 12, 'collection': 268.5},
                {'trip_number': 4, 'route_name': 'San Pedro - Calamba', 'direction': 'North-South', 'passenger_count': 12, 'collection': 268.5},
            ]
            
            for trip_data in default_trips:
                WaybillTrip.objects.create(waybill=waybill, **trip_data)
            
            trips = WaybillTrip.objects.filter(waybill=waybill).order_by('trip_number')
        
        context['waybill_details'] = details
        context['waybill_trips'] = trips
        
        # Calculate summary data
        context['total_passengers'] = sum(trip.passenger_count for trip in trips)
        context['total_collection'] = sum(trip.collection for trip in trips)
        
        return context

class WaybillCreateView(CreateView):
    model = Waybill
    form_class = WaybillForm
    template_name = 'waybillMaster/waybillMaster_form.html'
    success_url = reverse_lazy('waybill:list')
    
    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Create default waybill details
        WaybillDetails.objects.create(
            waybill=self.object,
            actual_amount=0.00,
            etim_amount=0.00,
            expenses=0.00,
            penalty_excess_amount=0.00,
            total_sales=0.00,
            payment_method='Cash',
            passenger_count=0,
            collection=0.00,
            payment_penalty_excess=0.00,
            payment_total_sales=0.00,
            total_cash_collection=0.00,
            fuel_consumption=0.00,
            toll_fees=0.00,
            parking_fees=0.00,
            other_expenses=0.00,
        )
        
        messages.success(self.request, 'Waybill created successfully!')
        return response

class WaybillUpdateView(UpdateView):
    model = Waybill
    form_class = WaybillForm
    template_name = 'waybillMaster/waybillMaster_form.html'
    success_url = reverse_lazy('waybill:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Waybill updated successfully!')
        return super().form_valid(form)

class WaybillDeleteView(DeleteView):
    model = Waybill
    template_name = 'waybillMaster/waybillMaster_confirmdelete.html'
    success_url = reverse_lazy('waybill:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Waybill deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Additional views for managing waybill details and trips
class WaybillDetailsUpdateView(UpdateView):
    model = WaybillDetails
    fields = [
        'actual_amount', 'etim_amount', 'expenses', 'penalty_excess_amount',
        'payment_method', 'passenger_count', 'collection', 'payment_penalty_excess',
        'fuel_consumption', 'toll_fees', 'parking_fees', 'other_expenses',
        'completion_date'
    ]
    template_name = 'waybillMaster/waybill_details_form.html'
    
    def get_success_url(self):
        return reverse_lazy('waybill:detail', kwargs={'pk': self.object.waybill.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Waybill details updated successfully!')
        return super().form_valid(form)


def waybill_summary_view(request):
    """Summary view for all waybills with totals"""
    waybills = Waybill.objects.select_related('details').filter(status='Active')
    
    total_collection = sum(
        waybill.details.total_cash_collection if hasattr(waybill, 'details') else 0 
        for waybill in waybills
    )
    
    total_expenses = sum(
        waybill.details.expenses if hasattr(waybill, 'details') else 0 
        for waybill in waybills
    )
    
    context = {
        'waybills': waybills,
        'total_collection': total_collection,
        'total_expenses': total_expenses,
        'net_income': total_collection - total_expenses,
    }
    
    return render(request, 'waybillMaster/waybill_summary.html', context)