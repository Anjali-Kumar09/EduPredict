from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from apps.students.models import Student
from apps.assignments.models import Assignment, Submission
from .predictor import predictor

# ==================== SINGLE STUDENT PREDICTION ====================
@login_required
@require_http_methods(['GET'])
def predict_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Get courses the student is enrolled in
    courses = [e.course for e in student.enrollment_set.filter(status='active')]
    
    # ----- REAL ATTENDANCE % (last 30 days) -----
    cutoff = timezone.now() - timedelta(days=30)
    att_records = student.attendances.filter(date__gte=cutoff)
    total_att = att_records.count()
    if total_att == 0:
        attendance_pct = 100.0
    else:
        present = att_records.filter(status=True).count()
        attendance_pct = (present / total_att) * 100

    # ----- REAL SUBMISSION RATE -----
    all_assignments = Assignment.objects.filter(course__in=courses)
    total_ass = all_assignments.count()
    if total_ass == 0:
        submission_rate = 0.0
    else:
        submitted = Submission.objects.filter(student=student, assignment__in=all_assignments).count()
        submission_rate = (submitted / total_ass) * 100

    # ----- FEATURE DICTIONARY -----
    income_map = {'low':0, 'medium':1, 'high':2, 'very_high':3}
    features = {
        'previous_cgpa': student.current_cgpa,
        'attendance': attendance_pct,
        'assignment_submission_rate': submission_rate,
        'study_hours_per_day': getattr(student, 'study_hours_per_day', 4.0),  # default if field missing
        'backlogs': student.backlog_count,
        'family_income': income_map.get(student.family_income, 1),
        'high_school_percentage': student.high_school_percentage,
        'entrance_score': student.entrance_exam_score or 100,
    }
    
    result = predictor.predict(features)
    return JsonResponse(result)


# ==================== BATCH CSV PREDICTION ====================
@staff_member_required
def batch_predict_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)
        
        required_cols = [
            'previous_cgpa', 'attendance', 'assignment_submission_rate',
            'study_hours_per_day', 'backlogs', 'family_income',
            'high_school_percentage', 'entrance_score'
        ]
        for col in required_cols:
            if col not in df.columns:
                return HttpResponse(f"Missing column: {col}", status=400)
        
        predictions = []
        for _, row in df.iterrows():
            features = {col: row[col] for col in required_cols}
            result = predictor.predict(features)
            predictions.append(result['predicted_cgpa'])
        
        df['predicted_cgpa'] = predictions
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="predictions.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response
    
    return render(request, 'ml_model/batch_predict.html')