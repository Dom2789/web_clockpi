from django.contrib import admin
from .models import TextFile, SelectedContent

@admin.register(TextFile)
class TextFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['name']

@admin.register(SelectedContent)
class SelectedContentAdmin(admin.ModelAdmin):
    list_display = ['text_file', 'line_number', 'content_preview', 'selected_at']
    list_filter = ['selected_at', 'text_file']
    search_fields = ['content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
