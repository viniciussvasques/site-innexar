from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint
    """
    return Response({
        'name': 'StructurOne API',
        'version': '0.1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'projects': '/api/projects/',
            'investors': '/api/investors/',
            'financial': '/api/financial/',
        }
    })

