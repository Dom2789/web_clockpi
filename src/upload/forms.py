# forms.py
from django import forms
from .models import TextFile
import os
from django.conf import settings

class FileSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get the directory path from settings
        text_files_dir = getattr(settings, 'TEXT_FILES_DIRECTORY', 'text_files')
        
        # Get list of .txt files from the directory
        file_choices = []
        try:
            if os.path.exists(text_files_dir):
                for filename in os.listdir(text_files_dir):
                    if filename.lower().endswith('.txt') and filename.lower().startswith("room_"):
                        file_path = os.path.join(text_files_dir, filename)
                        file_choices.append((file_path, filename))
            file_choices.sort(key=lambda x: x[1])  # Sort by filename
        except Exception as e:
            pass  # Handle directory access errors gracefully
            
        if not file_choices:
            file_choices = [('', 'No text files found in directory')]
            
        self.fields['selected_file'] = forms.ChoiceField(
            choices=file_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Select Text File'
        )

class ContentSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        file_lines = kwargs.pop('file_lines', [])
        start_line = kwargs.pop('start_line', 0)
        super().__init__(*args, **kwargs)
        
        for i, line in enumerate(file_lines):
            actual_line_number = start_line + i + 1
            self.fields[f'line_{start_line + i}'] = forms.BooleanField(
                required=False,
                label=f"Line {actual_line_number}: {line[:100]}{'...' if len(line) > 100 else ''}",
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )