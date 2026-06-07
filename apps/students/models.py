from django.db import models
from apps.accounts.models import User
from apps.academics.models import Department, Batch

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    enrollment_number = models.CharField(max_length=20, unique=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    semester = models.IntegerField(default=1)
    current_cgpa = models.FloatField(default=0.0)
    father_name = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    high_school_percentage = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"