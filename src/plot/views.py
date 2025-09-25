from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from upload.models import TextFile, SelectedContent  # Import from upload app
from .forms import FileSelectionForm
import json

def plot_selection(request):
    """View to select a file for plotting"""
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            file_id = form.cleaned_data['selected_file']
            if file_id:
                return redirect('plot_data', file_id=file_id)
            else:
                messages.error(request, "Please select a file to plot.")
    else:
        form = FileSelectionForm()
    
    # Get summary statistics for display
    total_files = TextFile.objects.count()
    total_selected_lines = SelectedContent.objects.count()
    
    context = {
        'form': form,
        'total_files': total_files,
        'total_selected_lines': total_selected_lines,
    }
    
    return render(request, 'plot/select_file.html', context)

def plot_data(request, file_id):
    """View to display plotting interface for selected file"""
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    if not selected_contents.exists():
        messages.warning(request, f"No selected content found for {text_file.name}")
        return redirect('plot_selection')
    
    # Prepare data for plotting
    plot_data = []
    for content in selected_contents:
        plot_data.append({
            'line_number': content.line_number,
            'content': content.content,
            'length': len(content.content),
            'word_count': len(content.content.split()) if content.content.strip() else 0
        })
    
    context = {
        'text_file': text_file,
        'selected_contents': selected_contents,
        'plot_data': json.dumps(plot_data),  # For JavaScript plotting
        'total_lines': len(plot_data),
    }
    
    return render(request, 'plot/plot_data.html', context)

def get_plot_data_api(request, file_id):
    """API endpoint to get plot data as JSON"""
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    data = []
    for content in selected_contents:
        # You can customize this data structure for your plotting needs
        data.append({
            'line_number': content.line_number,
            'content': content.content,
            'content_length': len(content.content),
            'word_count': len(content.content.split()) if content.content.strip() else 0,
            'selected_at': content.selected_at.isoformat(),
        })
    
    return JsonResponse({
        'file_name': text_file.name,
        'file_path': text_file.file_path,
        'data': data,
        'total_lines': len(data)
    })

def file_list_api(request):
    """API endpoint to get list of available files"""
    files = []
    for text_file in TextFile.objects.all():
        selected_count = text_file.selected_contents.count()
        files.append({
            'id': text_file.id,
            'name': text_file.name,
            'file_path': text_file.file_path,
            'selected_lines': selected_count,
            'processed_at': text_file.processed_at.isoformat()
        })
    
    return JsonResponse({'files': files})