"""
Tenants API URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.TenantViewSet, basename='tenant')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.tenant_stats, name='tenant_stats'),
]

