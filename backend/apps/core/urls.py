from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Register viewsets here

urlpatterns = [
    path('', views.api_root, name='api-root'),
] + router.urls

