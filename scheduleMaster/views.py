from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import ScheduleMaster
from .forms import ScheduleMasterForm

@login_required
def schedule_list(request):
    """Display list of schedules with search and pagination"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    schedules = ScheduleMaster.objects.all()
    
    if search_query:
        schedules = schedules.filter(
            Q(schedule_name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        schedules = schedules.filter(status=status_filter)
    
    paginator = Paginator(schedules, 10)  # Show 10 schedules per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    total_schedules = schedules.count()
    active_schedules = schedules.filter(status='Active').count()
    total_trips = sum(schedule.trips for schedule in schedules)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': ScheduleMaster.STATUS_CHOICES,
        'total_schedules': total_schedules,
        'active_schedules': active_schedules,
        'total_trips': total_trips,
    }
    
    return render(request, 'scheduleMaster/scheduleMaster_list.html', context)

@login_required
def schedule_create(request):
    """Create new schedule"""
    if request.method == 'POST':
        form = ScheduleMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule created successfully!')
            return redirect('scheduleMaster:list')
    else:
        form = ScheduleMasterForm()
    
    return render(request, 'scheduleMaster/scheduleMaster_form.html', {
        'form': form,
        'title': 'Create Schedule',
        'button_text': 'Create'
    })

@login_required
def schedule_update(request, pk):
    """Update existing schedule"""
    schedule = get_object_or_404(ScheduleMaster, pk=pk)
    
    if request.method == 'POST':
        form = ScheduleMasterForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated successfully!')
            return redirect('scheduleMaster:list')
    else:
        form = ScheduleMasterForm(instance=schedule)
    
    return render(request, 'scheduleMaster/scheduleMaster_form.html', {
        'form': form,
        'title': 'Update Schedule',
        'button_text': 'Update',
        'schedule': schedule
    })

@login_required
def schedule_detail(request, pk):
    """View schedule details"""
    schedule = get_object_or_404(ScheduleMaster, pk=pk)
    return render(request, 'scheduleMaster/scheduleMaster_detail.html', {'schedule': schedule})

@login_required
def schedule_delete(request, pk):
    """Delete schedule"""
    schedule = get_object_or_404(ScheduleMaster, pk=pk)
    if request.method == 'POST':
        schedule_name = schedule.schedule_name
        schedule.delete()
        messages.success(request, f'Schedule "{schedule_name}" deleted successfully!')
        return redirect('scheduleMaster:list')
    return render(request, 'scheduleMaster/scheduleMaster_confirmdelete.html', {'schedule': schedule})

@login_required
@require_http_methods(["POST"])
def schedule_toggle_status(request, pk):
    """Toggle schedule status via AJAX"""
    schedule = get_object_or_404(ScheduleMaster, pk=pk)
    schedule.status = 'Inactive' if schedule.status == 'Active' else 'Active'
    schedule.save()
    
    return JsonResponse({
        'success': True,
        'new_status': schedule.status,
        'message': f'Schedule status changed to {schedule.status}'
    })

@login_required
def schedule_duplicate(request, pk):
    """Duplicate an existing schedule"""
    original_schedule = get_object_or_404(ScheduleMaster, pk=pk)
    
    if request.method == 'POST':
        form = ScheduleMasterForm(request.POST)
        if form.is_valid():
            new_schedule = form.save()
            messages.success(request, f'Schedule duplicated successfully as "{new_schedule.schedule_name}"!')
            return redirect('scheduleMaster:list')
    else:
        # Pre-populate form with original data but modify the name
        initial_data = {
            'schedule_name': f"{original_schedule.schedule_name} (Copy)",
            'trips': original_schedule.trips,
            'start_time': original_schedule.start_time,
            'end_time': original_schedule.end_time,
            'description': original_schedule.description,
            'status': 'Active'
        }
        form = ScheduleMasterForm(initial=initial_data)
    
    return render(request, 'schedule_master/form.html', {
        'form': form,
        'title': f'Duplicate Schedule - {original_schedule.schedule_name}',
        'button_text': 'Create Copy'
    })