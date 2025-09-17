from django.db import models

class TextFile(models.Model):
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)  # Store relative path to the file
    processed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class SelectedContent(models.Model):
    text_file = models.ForeignKey(TextFile, on_delete=models.CASCADE, related_name='selected_contents')
    content = models.TextField()
    line_number = models.IntegerField(null=True, blank=True)
    selected_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Content from {self.text_file.name} - Line {self.line_number}"
