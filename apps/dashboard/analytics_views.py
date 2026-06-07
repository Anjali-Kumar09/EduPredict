from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Q
from apps.students.models import Student
from apps.grades.models import Grade

@staff_member_required
def admin_analytics(request):
    total_students = Student.objects.count()
    avg_cgpa = Student.objects.aggregate(Avg('current_cgpa'))['current_cgpa__avg'] or 0

    low_risk = Student.objects.filter(current_cgpa__gte=8.0).count()
    medium_risk = Student.objects.filter(current_cgpa__gte=5.0, current_cgpa__lt=8.0).count()
    high_risk = Student.objects.filter(current_cgpa__lt=5.0).count()

    semester_counts = Student.objects.values('semester').annotate(count=Count('id')).order_by('semester')
    total_grades = Grade.objects.count()
    avg_marks = Grade.objects.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0

    # Grade distribution (percentage ranges)
    if total_grades > 0:
        grades = Grade.objects.all()
        grade_below_40 = grades.filter(marks_obtained__lt=0.4 * 100).count()
        grade_40_59 = grades.filter(marks_obtained__gte=0.4 * 100, marks_obtained__lt=0.6 * 100).count()
        grade_60_79 = grades.filter(marks_obtained__gte=0.6 * 100, marks_obtained__lt=0.8 * 100).count()
        grade_80_100 = grades.filter(marks_obtained__gte=0.8 * 100).count()
    else:
        grade_below_40 = grade_40_59 = grade_60_79 = grade_80_100 = 0

    context = {
        'total_students': total_students,
        'avg_cgpa': round(avg_cgpa, 2),
        'low_risk': low_risk,
        'medium_risk': medium_risk,
        'high_risk': high_risk,
        'semester_counts': list(semester_counts),
        'total_grades': total_grades,
        'avg_marks': round(avg_marks, 2),
        # For grade distribution chart
        'grade_below_40': grade_below_40,
        'grade_40_59': grade_40_59,
        'grade_60_79': grade_60_79,
        'grade_80_100': grade_80_100,
    }
    return render(request, 'dashboard/admin_analytics.html', context)