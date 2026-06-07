from django.db import models
from apps.accounts.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Batch(models.Model):
    year = models.CharField(max_length=9)  # e.g., "2020-2024"
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_students = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.department.name} - {self.year}"

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credits = models.IntegerField()
    semester = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role':'teacher'})
    syllabus = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('active','Active'),('completed','Completed'),('dropped','Dropped')], default='active') 
    def __str__(self):
        return f"{self.student} - {self.course}"