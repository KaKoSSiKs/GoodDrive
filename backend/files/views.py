from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import File
from .serializers import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    
    def get_queryset(self):
        return File.objects.filter(uploaded_by=self.request.user)
    
    def perform_create(self, serializer):
        file_obj = self.request.FILES.get('file')
        if file_obj:
            serializer.save(
                uploaded_by=self.request.user,
                size=file_obj.size,
                file_type=file_obj.content_type
            )
        else:
            serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        file_obj = self.get_object()
        response = Response()
        response['Content-Disposition'] = f'attachment; filename="{file_obj.name}"'
        return response

