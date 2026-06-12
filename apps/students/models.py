from django.db import models
from apps.accounts.models import User
from apps.academics.models import Department, Batch

class Student(models.Model):
    INCOME_CHOICES = (
        ('low', 'Below 2.5 LPA'),
        ('medium', '2.5-5 LPA'),
        ('high', '5-10 LPA'),
        ('very_high', 'Above 10 LPA'),
    )

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
    
    # NEW: fields needed for ML prediction
    family_income = models.CharField(max_length=20, choices=INCOME_CHOICES, default='medium')
    backlog_count = models.IntegerField(default=0)
    entrance_exam_score = models.FloatField(null=True, blank=True)  # optional
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"