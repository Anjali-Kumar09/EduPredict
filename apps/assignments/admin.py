from django.contrib import admin
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'total_marks')
    list_filter = ('course', 'due_date')
    search_fields = ('title', 'course__code')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'marks_obtained', 'is_late')
    list_filter = ('assignment', 'is_late')
    search_fields = ('student__roll_number',)