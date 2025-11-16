"""
Documents API Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_list(request):
    """
    List all documents
    """
    return Response({'message': 'Documents list endpoint'})


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def document_detail(request, document_id):
    """
    Retrieve or delete a document
    """
    if request.method == 'GET':
        return Response({'message': f'Document {document_id} detail endpoint'})
    elif request.method == 'DELETE':
        return Response({'message': f'Delete document {document_id} endpoint'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def document_upload(request):
    """
    Upload a new document
    """
    return Response({'message': 'Document upload endpoint'})

