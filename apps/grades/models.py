from django.db import models
from apps.students.models import Student
from apps.academics.models import Course

class Grade(models.Model):
    EXAM_TYPES = (
        ('internal1', 'Internal Assessment 1'),
        ('internal2', 'Internal Assessment 2'),
        ('internal3', 'Internal Assessment 3'),
        ('external', 'End Semester Exam'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    marks_obtained = models.FloatField()
    maximum_marks = models.FloatField(default=100)
    semester = models.IntegerField()
    
    @property
    def percentage(self):
        return (self.marks_obtained / self.maximum_marks) * 100
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} - {self.exam_type}"
    
    class Meta:
        unique_together = ('student', 'course', 'exam_type')