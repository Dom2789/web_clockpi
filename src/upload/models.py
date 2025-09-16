from django.db import models

from django.db import models

class TextFile(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='text_files/')
    
    def __str__(self):
        return self.name

class SelectedContent(models.Model):
    text_file = models.ForeignKey(TextFile, on_delete=models.CASCADE, related_name='selected_contents')
    content = models.TextField()
    line_number = models.IntegerField(null=True, blank=True)
    selected_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Content from {self.text_file.name} - Line {self.line_number}"

# forms.py
from django import forms
from .models import TextFile

class TextFileUploadForm(forms.ModelForm):
    class Meta:
        model = TextFile
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter file name'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.txt'})
        }

class ContentSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        file_lines = kwargs.pop('file_lines', [])
        super().__init__(*args, **kwargs)
        
        for i, line in enumerate(file_lines):
            self.fields[f'line_{i}'] = forms.BooleanField(
                required=False,
                label=f"Line {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}",
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
