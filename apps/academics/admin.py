from django.contrib import admin
from .models import Department, Batch, Course, Enrollment

admin.site.register(Department)
admin.site.register(Batch)
admin.site.register(Course)
admin.site.register(Enrollment)