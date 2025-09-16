from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import TextFile, SelectedContent
from .forms import TextFileUploadForm, ContentSelectionForm
import os

def upload_file(request):
    if request.method == 'POST':
        form = TextFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = form.save()
            return redirect('view_file', file_id=text_file.id)
    else:
        form = TextFileUploadForm()
    
    return render(request, 'upload.html', {'form': form})

def view_file(request, file_id):
    text_file = get_object_or_404(TextFile, id=file_id)
    
    # Read file content
    try:
        with open(text_file.file.path, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()
        # Remove newline characters
        file_lines = [line.rstrip('\n\r') for line in file_lines]
    except Exception as e:
        messages.error(request, f"Error reading file: {str(e)}")
        return redirect('upload_file')
    
    if request.method == 'POST':
        form = ContentSelectionForm(request.POST, file_lines=file_lines)
        if form.is_valid():
            # Clear existing selected content for this file
            SelectedContent.objects.filter(text_file=text_file).delete()
            
            # Save selected lines
            selected_count = 0
            for i, line in enumerate(file_lines):
                if form.cleaned_data.get(f'line_{i}'):
                    SelectedContent.objects.create(
                        text_file=text_file,
                        content=line,
                        line_number=i + 1
                    )
                    selected_count += 1
            
            messages.success(request, f"Successfully saved {selected_count} selected lines to database!")
            return redirect('view_selected', file_id=file_id)
    else:
        form = ContentSelectionForm(file_lines=file_lines)
    
    return render(request, 'view_file.html', {
        'text_file': text_file,
        'form': form,
        'file_lines': file_lines
    })

def view_selected(request, file_id):
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    return render(request, 'view_selected.html', {
        'text_file': text_file,
        'selected_contents': selected_contents
    })

def file_list(request):
    files = TextFile.objects.all().order_by('-uploaded_at')
    return render(request, 'file_list.html', {'files': files})
