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