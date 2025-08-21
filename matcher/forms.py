from django import forms
from .models import JobDescription, Resume

# Custom widget to allow multiple file uploads
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ['title', 'description_text']

from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
