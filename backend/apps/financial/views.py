"""
Financial API Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    """
    List all transactions or create a new transaction
    """
    if request.method == 'GET':
        return Response({'message': 'Transactions list endpoint'})
    elif request.method == 'POST':
        return Response({'message': 'Create transaction endpoint'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, transaction_id):
    """
    Retrieve, update or delete a transaction
    """
    if request.method == 'GET':
        return Response({'message': f'Transaction {transaction_id} detail endpoint'})
    elif request.method == 'PUT':
        return Response({'message': f'Update transaction {transaction_id} endpoint'})
    elif request.method == 'DELETE':
        return Response({'message': f'Delete transaction {transaction_id} endpoint'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cashflow(request):
    """
    Get cashflow data
    """
    return Response({'message': 'Cashflow endpoint'})

