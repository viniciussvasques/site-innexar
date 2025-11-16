"""
Updates API Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_list(request):
    """
    List all updates or create a new update
    """
    if request.method == 'GET':
        return Response({'message': 'Updates list endpoint'})
    elif request.method == 'POST':
        return Response({'message': 'Create update endpoint'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_detail(request, update_id):
    """
    Retrieve, update or delete an update
    """
    if request.method == 'GET':
        return Response({'message': f'Update {update_id} detail endpoint'})
    elif request.method == 'PUT':
        return Response({'message': f'Update {update_id} endpoint'})
    elif request.method == 'DELETE':
        return Response({'message': f'Delete update {update_id} endpoint'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_updates(request, project_id):
    """
    Get all updates for a specific project
    """
    return Response({'message': f'Updates for project {project_id}'})

