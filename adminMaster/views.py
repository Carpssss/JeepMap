from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import AdminMaster
from .forms import AdminMasterForm
from django.contrib.auth.decorators import login_required


@login_required
def admin_list(request):
    admins = AdminMaster.objects.all().order_by('admin_id')
    return render(request, 'adminMaster/adminMaster_list.html', {'admins': admins})

@login_required
def admin_create(request):
    if request.method == 'POST':
        form = AdminMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin created successfully!')
            return redirect('admin_list')
    else:
        form = AdminMasterForm()
    return render(request, 'adminMaster/adminMaster_form.html', {'form': form, 'title': 'Create Admin'})

@login_required
def admin_update(request, pk):
    admin = get_object_or_404(AdminMaster, pk=pk)
    if request.method == 'POST':
        form = AdminMasterForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin updated successfully!')
            return redirect('admin_list')
    else:
        form = AdminMasterForm(instance=admin)
    return render(request, 'adminMaster/adminMaster_form.html', {'form': form, 'title': 'Update Admin', 'admin': admin})

@login_required
def admin_detail(request, pk):
    admin = get_object_or_404(AdminMaster, pk=pk)
    return render(request, 'adminMaster/adminMaster_detail.html', {'admin': admin})

@login_required
def admin_delete(request, pk):
    admin = get_object_or_404(AdminMaster, pk=pk)
    if request.method == 'POST':
        admin.delete()
        messages.success(request, 'Admin deleted successfully!')
        return redirect('admin_list')
    return render(request, 'adminMaster/adminMaster_confirmdelete.html', {'admin': admin})
