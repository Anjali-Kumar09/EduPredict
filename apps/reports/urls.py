from django.urls import path
from . import views

urlpatterns = [
    path('student/<int:student_id>/pdf/', views.student_report_pdf, name='student_report_pdf'),
    path('course/<int:course_id>/excel/', views.class_performance_excel, name='class_performance_excel'),
]