from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import TextFile, SelectedContent
from .forms import FileSelectionForm, ContentSelectionForm
import os

def select_file(request):
    """View to select a file from the server directory"""
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            selected_file_path = form.cleaned_data['selected_file']
            if selected_file_path and os.path.exists(selected_file_path):
                # Get filename without path
                filename = os.path.basename(selected_file_path)
                
                # Check if this file is already processed
                text_file, created = TextFile.objects.get_or_create(
                    file_path=selected_file_path,
                    defaults={'name': filename}
                )
                
                return redirect('view_file', file_id=text_file.id)
            else:
                messages.error(request, "Selected file not found or inaccessible.")
    else:
        form = FileSelectionForm()
    
    return render(request, 'select_file.html', {'form': form})

def view_file(request, file_id):
    text_file = get_object_or_404(TextFile, id=file_id)
    
    # Read file content from server directory
    try:
        if not os.path.exists(text_file.file_path):
            messages.error(request, f"File not found: {text_file.file_path}")
            return redirect('select_file')
            
        with open(text_file.file_path, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()
        # Remove newline characters
        file_lines = [line.rstrip('\n\r') for line in file_lines]
    except Exception as e:
        messages.error(request, f"Error reading file: {str(e)}")
        return redirect('select_file')
    
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
    files = TextFile.objects.all().order_by('-processed_at')
    return render(request, 'file_list.html', {'files': files})

def refresh_files(request):
    """View to scan directory and show available files without processing"""
    text_files_dir = getattr(settings, 'TEXT_FILES_DIRECTORY', 'text_files')
    available_files = []
    
    try:
        if os.path.exists(text_files_dir):
            for filename in os.listdir(text_files_dir):
                if filename.lower().endswith('.txt'):
                    file_path = os.path.join(text_files_dir, filename)
                    file_stat = os.stat(file_path)
                    available_files.append({
                        'name': filename,
                        'path': file_path,
                        'size': file_stat.st_size,
                        'modified': file_stat.st_mtime
                    })
            available_files.sort(key=lambda x: x['name'])
    except Exception as e:
        messages.error(request, f"Error accessing directory: {str(e)}")
    
    return render(request, 'refresh_files.html', {
        'available_files': available_files,
        'directory': text_files_dir
    })