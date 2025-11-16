"""
StructurOne URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Admin URLs
admin.site.site_header = "StructurOne Admin"
admin.site.site_title = "StructurOne Admin Portal"
admin.site.index_title = "Welcome to StructurOne Administration"

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Custom Admin Panel (if needed)
    path('admin-panel/', include('apps.admin.urls')),
    
    # API Backend
    path('api/', include('apps.core.urls')),
    path('api/auth/', include('apps.core.auth_urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/investors/', include('apps.investors.urls')),
    path('api/financial/', include('apps.financial.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/updates/', include('apps.updates.urls')),
]

# i18n patterns for frontend (if using Django templates)
urlpatterns += i18n_patterns(
    path('', include('apps.core.frontend_urls')),
)

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
