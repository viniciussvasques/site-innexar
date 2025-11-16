"""
Financial API URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('cashflow/', views.cashflow, name='cashflow'),
]

