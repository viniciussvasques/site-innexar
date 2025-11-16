"""
Investors API Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def investor_list(request):
    """
    List all investors or create a new investor
    """
    if request.method == 'GET':
        return Response({'message': 'Investors list endpoint'})
    elif request.method == 'POST':
        return Response({'message': 'Create investor endpoint'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def investor_detail(request, investor_id):
    """
    Retrieve, update or delete an investor
    """
    if request.method == 'GET':
        return Response({'message': f'Investor {investor_id} detail endpoint'})
    elif request.method == 'PUT':
        return Response({'message': f'Update investor {investor_id} endpoint'})
    elif request.method == 'DELETE':
        return Response({'message': f'Delete investor {investor_id} endpoint'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investor_investments(request, investor_id):
    """
    Get investments for a specific investor
    """
    return Response({'message': f'Investments for investor {investor_id}'})

