"""
Updates API URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.update_list, name='update_list'),
    path('<int:update_id>/', views.update_detail, name='update_detail'),
    path('project/<int:project_id>/', views.project_updates, name='project_updates'),
]

