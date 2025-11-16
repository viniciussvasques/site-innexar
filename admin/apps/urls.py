"""
Admin Panel URLs
Custom admin panel routes
"""
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tenants/', views.tenants_list, name='tenants_list'),
    path('tenants/<int:tenant_id>/', views.tenant_detail, name='tenant_detail'),
    path('users/', views.users_list, name='users_list'),
    path('settings/', views.settings_view, name='settings'),
]

