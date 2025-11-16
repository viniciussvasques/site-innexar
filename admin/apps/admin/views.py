"""
Admin Panel Views
Custom admin panel views
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def dashboard(request):
    """
    Admin dashboard
    """
    context = {
        'title': 'Admin Dashboard',
    }
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def tenants_list(request):
    """
    List all tenants
    """
    context = {
        'title': 'Tenants Management',
    }
    return render(request, 'admin/tenants_list.html', context)


@staff_member_required
def tenant_detail(request, tenant_id):
    """
    Tenant detail view
    """
    context = {
        'title': 'Tenant Detail',
        'tenant_id': tenant_id,
    }
    return render(request, 'admin/tenant_detail.html', context)


@staff_member_required
def users_list(request):
    """
    List all users
    """
    context = {
        'title': 'Users Management',
    }
    return render(request, 'admin/users_list.html', context)


@staff_member_required
def settings_view(request):
    """
    Admin settings
    """
    context = {
        'title': 'Admin Settings',
    }
    return render(request, 'admin/settings.html', context)

