from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Vehicle
from .forms import VehicleForm, VehicleSearchForm

def vehicle_list(request):
    search_form = VehicleSearchForm(request.GET)
    vehicles = Vehicle.objects.all()
    
    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        if search_query:
            vehicles = vehicles.filter(
                Q(vehicle_number__icontains=search_query) |
                Q(vehicle_type__icontains=search_query) |
                Q(vehicle_owner__icontains=search_query)
            )
    
    paginator = Paginator(vehicles, 25)  # Show 25 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_vehicles': vehicles.count(),
    }
    return render(request, 'vehicleMaster/vehicleMaster_list.html', context)

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'vehicleMaster/vehicleMaster_detail.html', {'vehicle': vehicle})

def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle {vehicle.vehicle_number} created successfully!')
            return redirect('vehicle_master:vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicleMaster/vehicleMaster_form.html', {
        'form': form,
        'title': 'Add New Vehicle',
        'button_text': 'Create Vehicle'
    })

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle {vehicle.vehicle_number} updated successfully!')
            return redirect('vehicle_master:vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicleMaster/vehicleMaster_form.html', {
        'form': form,
        'vehicle': vehicle,
        'title': f'Edit Vehicle {vehicle.vehicle_number}',
        'button_text': 'Update Vehicle'
    })

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle_number = vehicle.vehicle_number
        vehicle.delete()
        messages.success(request, f'Vehicle {vehicle_number} deleted successfully!')
        return redirect('vehicle_master:vehicle_list')
    
    return render(request, 'vehicleMaster/vehicleMaster_confirmdelete.html', {'vehicle': vehicle})
