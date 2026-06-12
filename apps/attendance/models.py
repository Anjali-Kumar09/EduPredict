from django.db import models
from apps.students.models import Student

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)  # True = Present, False = Absent
    subject = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.student.roll_number} - {self.date} - {'Present' if self.status else 'Absent'}"