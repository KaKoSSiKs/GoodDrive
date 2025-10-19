from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_by', 'uploaded_at', 'size', 'file_type']
    list_filter = ['uploaded_at', 'file_type']
    search_fields = ['name', 'uploaded_by__username']

