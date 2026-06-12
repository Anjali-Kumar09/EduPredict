from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Avg
from datetime import timedelta
from apps.academics.models import Enrollment, Course
from apps.assignments.models import Assignment, Submission
from apps.grades.models import Grade
from apps.students.models import Student
from apps.ml_model.predictor import predictor

# ---------- Helper functions ----------
def get_attendance_percentage(student, days=30):
    """Calculate attendance % for last `days` days (default 30)."""
    cutoff = timezone.now() - timedelta(days=days)
    records = student.attendances.filter(date__gte=cutoff)
    total = records.count()
    if total == 0:
        return 100.0          # default if no attendance records
    present = records.filter(status=True).count()
    return (present / total) * 100

def get_submission_rate(student, courses):
    """Calculate % of assignments submitted by student in given courses."""
    from apps.assignments.models import Assignment, Submission
    all_assignments = Assignment.objects.filter(course__in=courses)
    total = all_assignments.count()
    if total == 0:
        return 0.0
    submitted = Submission.objects.filter(student=student, assignment__in=all_assignments).count()
    return (submitted / total) * 100
# -------------------------------------

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
        if not recommendations:
            recommendations = ["✅ Keep up the good work! Maintain your study routine."]

        # ---------- ML PREDICTION with REAL data ----------
        income_map = {'low':0, 'medium':1, 'high':2, 'very_high':3}
        try:
            attendance_pct = get_attendance_percentage(student)
            submission_rate = get_submission_rate(student, courses)
            features = {
                'previous_cgpa': student.current_cgpa,
                'attendance': attendance_pct,
                'assignment_submission_rate': submission_rate,
                'study_hours_per_day': getattr(student, 'study_hours_per_day', 4.0),   # default if field missing
                'backlogs': student.backlog_count,
                'family_income': income_map.get(student.family_income, 1),
                'high_school_percentage': student.high_school_percentage,
                'entrance_score': student.entrance_exam_score or 100,
            }
            pred_result = predictor.predict(features)
        except Exception as e:
            pred_result = None
            print(f"Prediction error for student {student.id}: {e}")
        # -------------------------------------------------

        context = {
            'student': student,
            'courses': courses,
            'pending_assignments': pending_assignments,
            'recent_grades': recent_grades,
            'semester_cgpa': semester_cgpa,
            'performance_status': performance_status,
            'status_color': status_color,
            'recommendations': recommendations,
            'prediction': pred_result,
        }
        return render(request, 'dashboard/student_dashboard.html', context)

    elif role == 'teacher':
        courses = Course.objects.filter(teacher=user)
        at_risk_students = Student.objects.filter(
            enrollment__course__in=courses,
            enrollment__status='active',
            current_cgpa__lt=5.0
        ).distinct()
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