from django.db import models
from django.conf import settings
from apps.academics.models import Course
from apps.students.models import Student

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    total_marks = models.IntegerField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    class Meta:
        ordering = ['due_date']

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    marks_obtained = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    is_late = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.assignment.title}"
    
    class Meta:
        unique_together = ('assignment', 'student')  # one submission per assignment per student