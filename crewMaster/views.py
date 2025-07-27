from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CrewMaster
from .forms import CrewMasterForm, CrewMasterUpdateForm, PasswordChangeForm

@login_required
def crew_list(request):
    """Display list of crew members with search and pagination"""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    crews = CrewMaster.objects.all()
    
    if search_query:
        crews = crews.filter(
            Q(crew_id__icontains=search_query) | 
            Q(crew_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if role_filter:
        crews = crews.filter(role=role_filter)
    
    if status_filter:
        crews = crews.filter(status=status_filter)
    
    paginator = Paginator(crews, 10)  # Show 10 crews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'role_choices': CrewMaster.ROLE_CHOICES,
        'status_choices': CrewMaster.STATUS_CHOICES,
    }
    
    return render(request, 'crewMaster/crewMaster_list.html', context)

@login_required
def crew_create(request):
    """Create new crew member with QR code generation"""
    if request.method == 'POST':
        form = CrewMasterForm(request.POST)
        if form.is_valid():
            crew = form.save()
            messages.success(
                request, 
                f'Crew member "{crew.crew_name}" created successfully! QR code has been generated.'
            )
            return redirect('crew_master:detail', pk=crew.pk)  # Redirect to detail to show QR code
    else:
        form = CrewMasterForm()
    
    return render(request, 'crewMaster/crewMaster_form.html', {
        'form': form,
        'title': 'Create Crew Member',
        'button_text': 'Create'
    })

@login_required
def crew_update(request, pk):
    """Update existing crew member"""
    crew = get_object_or_404(CrewMaster, pk=pk)
    
    if request.method == 'POST':
        form = CrewMasterUpdateForm(request.POST, instance=crew)
        if form.is_valid():
            old_email = crew.email
            updated_crew = form.save()
            
            # Regenerate QR code if email changed
            if old_email != updated_crew.email:
                updated_crew.generate_qr_code()
                updated_crew.save(update_fields=['qr_code'])
                messages.success(request, 'Crew member updated and QR code regenerated!')
            else:
                messages.success(request, 'Crew member updated successfully!')
            
            return redirect('crew_master:detail', pk=updated_crew.pk)
    else:
        form = CrewMasterUpdateForm(instance=crew)
    
    return render(request, 'crewMaster/crewMaster_form.html', {
        'form': form,
        'title': 'Update Crew Member',
        'button_text': 'Update',
        'crew': crew
    })

@login_required
def crew_detail(request, pk):
    """View crew member details with QR code"""
    crew = get_object_or_404(CrewMaster, pk=pk)
    return render(request, 'crewMaster/crewMaster_detail.html', {'crew': crew})

@login_required
def crew_delete(request, pk):
    crew = get_object_or_404(CrewMaster, pk=pk)
    if request.method == 'POST':
        crew_name = crew.crew_name
        crew.delete()
        messages.success(request, f'Crew member "{crew_name}" deleted successfully!')
        return redirect('crew_master:crew_master_list')
    return render(request, 'crewMaster/crewMaster_confirmdelete.html', {'crew': crew})

@login_required
@require_http_methods(["POST"])
def crew_toggle_status(request, pk):
    """Toggle crew status via AJAX"""
    crew = get_object_or_404(CrewMaster, pk=pk)
    crew.status = 'Inactive' if crew.status == 'Active' else 'Active'
    crew.save()
    
    return JsonResponse({
        'success': True,
        'new_status': crew.status,
        'message': f'Status changed to {crew.status}'
    })

@login_required
def crew_password_change(request, pk):
    """Change crew member password"""
    crew = get_object_or_404(CrewMaster, pk=pk)
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            crew.set_password(form.cleaned_data['new_password'])
            crew.save(update_fields=['password'])
            messages.success(request, 'Password changed successfully!')
            return redirect('crew_master:detail', pk=crew.pk)
    else:
        form = PasswordChangeForm()
    
    return render(request, 'crewMaster/password_change.html', {
        'form': form,
        'crew': crew
    })

@login_required
def download_qr_code(request, pk):
    """Download QR code as PNG file"""
    crew = get_object_or_404(CrewMaster, pk=pk)
    
    if crew.qr_code:
        response = HttpResponse(crew.qr_code.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{crew.crew_id}_qr_code.png"'
        return response
    else:
        messages.error(request, 'QR code not found!')
        return redirect('crew_master:detail', pk=pk)

@login_required
def regenerate_qr_code(request, pk):
    """Regenerate QR code for crew member"""
    crew = get_object_or_404(CrewMaster, pk=pk)
    
    if request.method == 'POST':
        crew.generate_qr_code()
        crew.save(update_fields=['qr_code'])
        messages.success(request, 'QR code regenerated successfully!')
    
    return redirect('crew_master:detail', pk=pk)
