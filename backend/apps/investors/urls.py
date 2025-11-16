"""
Investors API URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.investor_list, name='investor_list'),
    path('<int:investor_id>/', views.investor_detail, name='investor_detail'),
    path('<int:investor_id>/investments/', views.investor_investments, name='investor_investments'),
]

