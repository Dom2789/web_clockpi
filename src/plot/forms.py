from django import forms
from upload.models import TextFile  # Import from your upload app

class FileSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all processed files from the upload app
        file_choices = []
        text_files = TextFile.objects.all().order_by('name')
        
        for text_file in text_files:
            # Show file name and number of selected lines
            selected_count = text_file.selected_contents.count()
            display_name = f"{text_file.name} ({selected_count} selected lines)"
            file_choices.append((text_file.id, display_name))
        
        if not file_choices:
            file_choices = [('', 'No processed files available')]
            
        self.fields['selected_file'] = forms.ChoiceField(
            choices=file_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Select File to Plot',
            #empty_label="Choose a file..."
        )