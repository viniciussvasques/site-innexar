"""
StructurOne Backend API URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Backend API URLs only
urlpatterns = [
    # API Backend
    path('api/', include('apps.core.urls')),
    path('api/auth/', include('apps.core.auth_urls')),
    path('api/tenants/', include('apps.tenants.urls')),  # Tenants API
    path('api/projects/', include('apps.projects.urls')),
    path('api/investors/', include('apps.investors.urls')),
    path('api/financial/', include('apps.financial.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/updates/', include('apps.updates.urls')),
]

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
