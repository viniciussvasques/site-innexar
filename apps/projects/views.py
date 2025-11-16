"""
Projects API Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def project_list(request):
    """
    List all projects or create a new project
    """
    if request.method == 'GET':
        # TODO: Implement list logic
        return Response({'message': 'Projects list endpoint'})
    elif request.method == 'POST':
        # TODO: Implement create logic
        return Response({'message': 'Create project endpoint'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_detail(request, project_id):
    """
    Retrieve, update or delete a project
    """
    if request.method == 'GET':
        # TODO: Implement detail logic
        return Response({'message': f'Project {project_id} detail endpoint'})
    elif request.method == 'PUT':
        # TODO: Implement update logic
        return Response({'message': f'Update project {project_id} endpoint'})
    elif request.method == 'DELETE':
        # TODO: Implement delete logic
        return Response({'message': f'Delete project {project_id} endpoint'})

