"""
Django Admin Customization
"""
from django.contrib import admin
from django.contrib.admin import AdminSite


class StructurOneAdminSite(AdminSite):
    """
    Custom Admin Site for StructurOne
    """
    site_header = "StructurOne Administration"
    site_title = "StructurOne Admin"
    index_title = "Welcome to StructurOne Administration"


# Create custom admin site instance
structurone_admin = StructurOneAdminSite(name='structurone_admin')

