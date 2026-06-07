from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import models
from django.db.models import Avg
from apps.academics.models import Enrollment, Course
from apps.assignments.models import Assignment, Submission
from apps.grades.models import Grade
from apps.students.models import Student

@login_required
def dashboard(request):
    user = request.user
    role = user.role

    if role == 'student':
        try:
            student = user.student_profile
        except Student.DoesNotExist:
            messages.warning(request, "Student profile not found. Contact admin.")
            return redirect('logout')
        
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        courses = [e.course for e in enrollments]
        pending_assignments = Assignment.objects.filter(
            course__in=courses,
            due_date__gte=timezone.now()
        ).exclude(submissions__student=student).order_by('due_date')
        recent_grades = Grade.objects.filter(student=student).order_by('-id')[:5]

        # Academic Progress (semester-wise CGPA)
        semester_cgpa = (Grade.objects.filter(student=student)
                         .values('semester')
                         .annotate(avg_marks=Avg('marks_obtained'))
                         .order_by('semester'))
        for item in semester_cgpa:
            item['cgpa'] = round(item['avg_marks'] / 10, 1)

        # Performance Status
        cgpa = student.current_cgpa
        if cgpa >= 8.0:
            performance_status = "Excellent"
            status_color = "success"
        elif cgpa >= 6.0:
            performance_status = "Good"
            status_color = "primary"
        elif cgpa >= 5.0:
            performance_status = "Average"
            status_color = "warning"
        else:
            performance_status = "At‑Risk"
            status_color = "danger"

        # Recommendations
        recommendations = []
        if pending_assignments.count() > 0:
            recommendations.append(f"📝 You have {pending_assignments.count()} pending assignment(s). Submit them soon.")
        if cgpa < 5.0:
            recommendations.append("⚠️ Your CGPA is low. Contact your academic advisor.")
        # Attendance model not yet implemented – skip
        # if hasattr(student, 'attendance_set') and not student.attendance_set.filter(status=True).exists():
        #     recommendations.append("📅 No attendance records found. Make sure you attend classes regularly.")
        if not recommendations:
            recommendations = ["✅ Keep up the good work! Maintain your study routine."]

        context = {
            'student': student,
            'courses': courses,
            'pending_assignments': pending_assignments,
            'recent_grades': recent_grades,
            'semester_cgpa': semester_cgpa,
            'performance_status': performance_status,
            'status_color': status_color,
            'recommendations': recommendations,
        }
        return render(request, 'dashboard/student_dashboard.html', context)

    elif role == 'teacher':
        courses = Course.objects.filter(teacher=user)

        # At‑Risk Students (CGPA < 5.0) – backlog_count does not exist
        at_risk_students = Student.objects.filter(
            enrollment__course__in=courses,
            enrollment__status='active',
            current_cgpa__lt=5.0
        ).distinct()

        # Pending Grading Count
        pending_grading_count = Submission.objects.filter(
            assignment__course__in=courses,
            marks_obtained__isnull=True
        ).count()

        recent_submissions = Submission.objects.filter(
            assignment__course__in=courses
        ).select_related('assignment', 'student').order_by('-submitted_at')[:10]
        
        context = {
            'courses': courses,
            'recent_submissions': recent_submissions,
            'at_risk_students': at_risk_students,
            'pending_grading_count': pending_grading_count,
        }
        return render(request, 'dashboard/teacher_dashboard.html', context)

    else:
        return redirect('/admin/')