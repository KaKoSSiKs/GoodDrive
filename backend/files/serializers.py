from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'uploaded_by', 'uploaded_at', 'size', 'file_type']
        read_only_fields = ['uploaded_by', 'uploaded_at', 'size', 'file_type']

