from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from upload.models import TextFile, SelectedContent
from .forms import FileSelectionForm
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import io
import base64
import json
from collections import Counter
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def plot_selection(request):
    """View to select a file for plotting"""
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            file_id = form.cleaned_data['selected_file']
            if file_id:
                return redirect('plot:plot_data', file_id=file_id)
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
        return redirect('plot:plot_selection')
    
    # Generate all plots
    plots = {}
    plots['line_length'] = generate_line_length_plot(selected_contents)
    plots['word_count'] = generate_word_count_plot(selected_contents)
    plots['distribution'] = generate_distribution_plot(selected_contents)
    plots['position_analysis'] = generate_position_analysis_plot(selected_contents)
    
    # Prepare data for custom plotting function
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
        'plots': plots,
        'plot_data': json.dumps(plot_data),
        'total_lines': len(plot_data),
    }
    
    return render(request, 'plot/plot_data.html', context)

def generate_line_length_plot(selected_contents):
    """Generate line length analysis plot"""
    plt.figure(figsize=(12, 6))
    
    line_numbers = [content.line_number for content in selected_contents]
    lengths = [len(content.content) for content in selected_contents]
    
    # Create subplot with two plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Line lengths over position
    ax1.plot(line_numbers, lengths, marker='o', alpha=0.7, linewidth=2, markersize=4)
    ax1.set_xlabel('Line Number')
    ax1.set_ylabel('Character Count')
    ax1.set_title('Line Length Distribution')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Histogram of lengths
    ax2.hist(lengths, bins=30, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Character Count')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Line Length Histogram')
    ax2.grid(True, alpha=0.3)
    
    # Add statistics
    avg_length = np.mean(lengths)
    ax1.axhline(y=avg_length, color='red', linestyle='--', alpha=0.7, label=f'Average: {avg_length:.1f}')
    ax1.legend()
    
    plt.tight_layout()
    return plot_to_base64()

def generate_word_count_plot(selected_contents):
    """Generate word count analysis plot"""
    plt.figure(figsize=(12, 6))
    
    line_numbers = [content.line_number for content in selected_contents]
    word_counts = [len(content.content.split()) if content.content.strip() else 0 for content in selected_contents]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Word counts over position
    ax1.scatter(line_numbers, word_counts, alpha=0.6, s=30)
    ax1.set_xlabel('Line Number')
    ax1.set_ylabel('Word Count')
    ax1.set_title('Word Count per Line')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Box plot of word counts
    ax2.boxplot(word_counts, vert=True)
    ax2.set_ylabel('Word Count')
    ax2.set_title('Word Count Distribution')
    ax2.grid(True, alpha=0.3)
    
    # Add statistics
    avg_words = np.mean(word_counts)
    ax1.axhline(y=avg_words, color='red', linestyle='--', alpha=0.7, label=f'Average: {avg_words:.1f}')
    ax1.legend()
    
    plt.tight_layout()
    return plot_to_base64()

def generate_distribution_plot(selected_contents):
    """Generate content distribution analysis"""
    plt.figure(figsize=(12, 8))
    
    # Analyze content patterns
    lengths = [len(content.content) for content in selected_contents]
    word_counts = [len(content.content.split()) if content.content.strip() else 0 for content in selected_contents]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Length vs Word Count correlation
    ax1.scatter(lengths, word_counts, alpha=0.6)
    ax1.set_xlabel('Character Count')
    ax1.set_ylabel('Word Count')
    ax1.set_title('Character Count vs Word Count')
    ax1.grid(True, alpha=0.3)
    
    # Add correlation line
    if len(lengths) > 1:
        z = np.polyfit(lengths, word_counts, 1)
        p = np.poly1d(z)
        ax1.plot(lengths, p(lengths), "r--", alpha=0.8)
    
    # Plot 2: Average words per character
    avg_chars_per_word = [length/word_count if word_count > 0 else 0 for length, word_count in zip(lengths, word_counts)]
    ax2.hist(avg_chars_per_word, bins=20, alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Average Characters per Word')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Character/Word Ratio Distribution')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Cumulative line count
    line_numbers = [content.line_number for content in selected_contents]
    ax3.plot(range(1, len(line_numbers) + 1), sorted(line_numbers), marker='o', markersize=3)
    ax3.set_xlabel('Selection Order')
    ax3.set_ylabel('Original Line Number')
    ax3.set_title('Selected Lines Distribution')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Content length trends
    ax4.plot(range(len(lengths)), lengths, alpha=0.7, linewidth=2)
    ax4.set_xlabel('Selection Index')
    ax4.set_ylabel('Character Count')
    ax4.set_title('Length Trend Across Selections')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plot_to_base64()

def generate_position_analysis_plot(selected_contents):
    """Generate position analysis of selected lines"""
    plt.figure(figsize=(12, 6))
    
    line_numbers = [content.line_number for content in selected_contents]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Line positions
    ax1.scatter(line_numbers, range(len(line_numbers)), alpha=0.6, s=30)
    ax1.set_xlabel('Original Line Number')
    ax1.set_ylabel('Selection Order')
    ax1.set_title('Selection Pattern Analysis')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Gap analysis
    if len(line_numbers) > 1:
        gaps = [line_numbers[i] - line_numbers[i-1] for i in range(1, len(line_numbers))]
        ax2.bar(range(len(gaps)), gaps, alpha=0.7)
        ax2.set_xlabel('Gap Index')
        ax2.set_ylabel('Line Number Gap')
        ax2.set_title('Gaps Between Selected Lines')
        ax2.grid(True, alpha=0.3)
        
        # Add average gap line
        if gaps:
            avg_gap = np.mean(gaps)
            ax2.axhline(y=avg_gap, color='red', linestyle='--', alpha=0.7, label=f'Average Gap: {avg_gap:.1f}')
            ax2.legend()
    else:
        ax2.text(0.5, 0.5, 'Not enough data\nfor gap analysis', 
                ha='center', va='center', transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Gap Analysis')
    
    plt.tight_layout()
    return plot_to_base64()

def plot_to_base64():
    """Convert current matplotlib plot to base64 string"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()  # Important: close the figure to free memory
    return image_base64

def custom_plot_view(request, file_id):
    """View for custom plotting function - placeholder for your function"""
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    if not selected_contents.exists():
        messages.warning(request, f"No selected content found for {text_file.name}")
        return redirect('plot:plot_selection')
    
    # Prepare data for your custom function
    data = []
    for content in selected_contents:
        data.append({
            'line_number': content.line_number,
            'content': content.content,
            'length': len(content.content),
            'word_count': len(content.content.split()) if content.content.strip() else 0
        })
    
    # Call your custom plotting function here
    custom_plot_base64 = your_custom_plot_function(data)  # Replace with your function
    
    context = {
        'text_file': text_file,
        'custom_plot': custom_plot_base64,
        'data_count': len(data)
    }
    
    return render(request, 'plot/custom_plot.html', context)

def your_custom_plot_function(data):
    """
    Placeholder for your custom plotting function
    Replace this with your actual plotting logic
    
    Args:
        data: List of dictionaries with line data
    
    Returns:
        base64 encoded image string
    """
    plt.figure(figsize=(10, 6))
    
    # Example custom plot - replace with your logic
    line_numbers = [item['line_number'] for item in data]
    lengths = [item['length'] for item in data]
    
    plt.plot(line_numbers, lengths, 'o-', alpha=0.7)
    plt.xlabel('Line Number')
    plt.ylabel('Content Length')
    plt.title('Custom Analysis Plot')
    plt.grid(True, alpha=0.3)
    
    # Add your custom analysis here
    # For example: trend analysis, pattern recognition, etc.
    
    return plot_to_base64()

def get_plot_data_api(request, file_id):
    """API endpoint to get plot data as JSON"""
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    data = []
    for content in selected_contents:
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

def download_plot(request, file_id, plot_type):
    """Download individual plots as PNG files"""
    text_file = get_object_or_404(TextFile, id=file_id)
    selected_contents = SelectedContent.objects.filter(text_file=text_file).order_by('line_number')
    
    if not selected_contents.exists():
        return HttpResponse("No data found", status=404)
    
    # Generate the requested plot
    if plot_type == 'line_length':
        plot_base64 = generate_line_length_plot(selected_contents)
    elif plot_type == 'word_count':
        plot_base64 = generate_word_count_plot(selected_contents)
    elif plot_type == 'distribution':
        plot_base64 = generate_distribution_plot(selected_contents)
    elif plot_type == 'position_analysis':
        plot_base64 = generate_position_analysis_plot(selected_contents)
    else:
        return HttpResponse("Invalid plot type", status=400)
    
    # Convert base64 back to image and return as download
    image_data = base64.b64decode(plot_base64)
    
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{text_file.name}_{plot_type}_plot.png"'
    
    return response