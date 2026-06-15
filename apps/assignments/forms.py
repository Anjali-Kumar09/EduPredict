from django import forms
from .models import Assignment, Submission
from apps.academics.models import Course

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt',
                'required': True   # forces browser to require a file
            })
        }

class AssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), empty_label="Select course")

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'total_marks', 'file']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher)