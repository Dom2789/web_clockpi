# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator
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
                print(filename)
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
    
    return render(request, 'upload/select_file.html', {'form': form})

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
    
    # Handle large files with pagination
    lines_per_page = 100  # Process 100 lines at a time
    page_number = request.GET.get('page', 1)
    
    # Create paginator
    paginator = Paginator(file_lines, lines_per_page)
    page_obj = paginator.get_page(page_number)
    
    # Get the starting line number for this page
    start_line = (page_obj.number - 1) * lines_per_page
    
    if request.method == 'POST':
        # Handle form submission for the current page
        form = ContentSelectionForm(request.POST, file_lines=page_obj.object_list, start_line=start_line)
        if form.is_valid():
            # Save selected lines for this page
            selected_count = 0
            for i, line in enumerate(page_obj.object_list):
                actual_line_number = start_line + i + 1
                field_name = f'line_{start_line + i}'
                
                if form.cleaned_data.get(field_name):
                    # Remove existing selection for this line if it exists
                    SelectedContent.objects.filter(
                        text_file=text_file,
                        line_number=actual_line_number
                    ).delete()
                    
                    # Create new selection
                    SelectedContent.objects.create(
                        text_file=text_file,
                        content=line,
                        line_number=actual_line_number
                    )
                    selected_count += 1
                else:
                    # Remove selection if unchecked
                    SelectedContent.objects.filter(
                        text_file=text_file,
                        line_number=actual_line_number
                    ).delete()
            
            messages.success(request, f"Updated selections for page {page_obj.number} ({selected_count} lines selected)")
            
            # Check if there's a next page or if user wants to finish
            if 'save_and_next' in request.POST and page_obj.has_next():
                return redirect(f"{request.path}?page={page_obj.next_page_number()}")
            elif 'save_and_finish' in request.POST:
                return redirect('view_selected', file_id=file_id)
            else:
                return redirect(f"{request.path}?page={page_obj.number}")
    else:
        form = ContentSelectionForm(file_lines=page_obj.object_list, start_line=start_line)
    
    # Get currently selected lines for this page
    selected_lines = set(
        SelectedContent.objects.filter(
            text_file=text_file,
            line_number__gte=start_line + 1,
            line_number__lte=start_line + len(page_obj.object_list)
        ).values_list('line_number', flat=True)
    )
    
    return render(request, 'upload/view_file.html', {
        'text_file': text_file,
        'form': form,
        'page_obj': page_obj,
        'file_lines': page_obj.object_list,
        'start_line': start_line,
        'selected_lines': selected_lines,
        'total_lines': len(file_lines)
    })

def view_selected(request, file_id):
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    return render(request, 'upload/view_selected.html', {
        'text_file': text_file,
        'selected_contents': selected_contents
    })

def file_list(request):
    files = TextFile.objects.all().order_by('-processed_at')
    return render(request, 'upload/file_list.html', {'files': files})

def refresh_files(request):
    """View to scan directory and show available files without processing"""
    text_files_dir = getattr(settings, 'TEXT_FILES_DIRECTORY', 'text_files')
    available_files = []
    
    try:
        if os.path.exists(text_files_dir):
            for filename in os.listdir(text_files_dir):
                if filename.lower().endswith('.txt') and filename.lower().startswith("room_"):
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
    
    return render(request, 'upload/refresh_files.html', {
        'available_files': available_files,
        'directory': text_files_dir
    })

def select_all_lines(request, file_id):
    """AJAX view to select all lines in the file"""
    if request.method == 'POST':
        text_file = get_object_or_404(TextFile, id=file_id)
        
        try:
            with open(text_file.file_path, 'r', encoding='utf-8') as f:
                file_lines = f.readlines()
            file_lines = [line.rstrip('\n\r') for line in file_lines]
            
            # Clear existing selections
            SelectedContent.objects.filter(text_file=text_file).delete()
            
            # Select all lines
            for i, line in enumerate(file_lines):
                SelectedContent.objects.create(
                    text_file=text_file,
                    content=line,
                    line_number=i + 1
                )
            
            return JsonResponse({
                'success': True, 
                'message': f'Selected all {len(file_lines)} lines'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def clear_all_selections(request, file_id):
    """AJAX view to clear all selections"""
    if request.method == 'POST':
        text_file = get_object_or_404(TextFile, id=file_id)
        count = SelectedContent.objects.filter(text_file=text_file).count()
        SelectedContent.objects.filter(text_file=text_file).delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Cleared {count} selections'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
