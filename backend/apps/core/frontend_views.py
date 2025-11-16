"""
Frontend Views
Views for frontend web interface (if using Django templates)
Note: For Next.js frontend, these won't be used - API will be consumed directly
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Home page
    """
    context = {
        'title': 'StructurOne - Gestão de Empreendimentos',
    }
    return render(request, 'frontend/home.html', context)


def login_view(request):
    """
    Login page
    """
    context = {
        'title': 'Login - StructurOne',
    }
    return render(request, 'frontend/login.html', context)


@login_required
def dashboard(request):
    """
    User dashboard
    """
    context = {
        'title': 'Dashboard - StructurOne',
    }
    return render(request, 'frontend/dashboard.html', context)


@login_required
def projects_list(request):
    """
    Projects list
    """
    context = {
        'title': 'Projetos - StructurOne',
    }
    return render(request, 'frontend/projects_list.html', context)


@login_required
def project_detail(request, project_id):
    """
    Project detail
    """
    context = {
        'title': 'Detalhes do Projeto - StructurOne',
        'project_id': project_id,
    }
    return render(request, 'frontend/project_detail.html', context)


@login_required
def investors_portal(request):
    """
    Investors portal
    """
    context = {
        'title': 'Portal do Investidor - StructurOne',
    }
    return render(request, 'frontend/investors_portal.html', context)

