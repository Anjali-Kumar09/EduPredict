from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'exam_type', 'marks_obtained', 'percentage')
    list_filter = ('exam_type', 'course')
    search_fields = ('student__roll_number',)