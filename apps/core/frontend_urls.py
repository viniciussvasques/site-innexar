"""
Frontend URLs
URLs for frontend web interface (if using Django templates)
"""
from django.urls import path
from . import frontend_views

app_name = 'frontend'

urlpatterns = [
    path('', frontend_views.home, name='home'),
    path('login/', frontend_views.login_view, name='login'),
    path('dashboard/', frontend_views.dashboard, name='dashboard'),
    path('projects/', frontend_views.projects_list, name='projects_list'),
    path('projects/<int:project_id>/', frontend_views.project_detail, name='project_detail'),
    path('investors/', frontend_views.investors_portal, name='investors_portal'),
]

