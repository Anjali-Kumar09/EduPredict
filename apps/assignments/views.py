from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, Submission
from .forms import SubmissionForm, AssignmentForm
from apps.students.models import Student
from apps.academics.models import Course

# ==================== STUDENT SUBMISSION (UPDATED WITH FILE CHECK) ====================
@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role != 'student':
        messages.error(request, "Only students can submit assignments.")
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('dashboard')
    
    if not student.enrollment_set.filter(course=assignment.course, status='active').exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('dashboard')
    
    existing = Submission.objects.filter(assignment=assignment, student=student).first()
    if existing:
        messages.warning(request, "You have already submitted. You can edit your submission.")
        return redirect('edit_submission', submission_id=existing.id)
    
    if request.method == 'POST':
        # ----- SERVER‑SIDE FILE VALIDATION -----
        if request.FILES.get('file') is None:
            messages.error(request, "Please select a file to upload.")
            form = SubmissionForm()
            return render(request, 'assignments/submit.html', {'assignment': assignment, 'form': form})
        
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = student
            if timezone.now() > assignment.due_date:
                submission.is_late = True
            submission.save()
            messages.success(request, "Assignment submitted successfully.")
            return redirect('dashboard')
    else:
        form = SubmissionForm()
    
    context = {'assignment': assignment, 'form': form}
    return render(request, 'assignments/submit.html', context)


# ==================== EDIT SUBMISSION ====================
@login_required
def edit_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.user.role != 'student' or request.user.student_profile != submission.student:
        messages.error(request, "You are not allowed to edit this submission.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            if timezone.now() > submission.assignment.due_date:
                submission.is_late = True
            submission.save()
            messages.success(request, "Submission updated.")
            return redirect('dashboard')
    else:
        form = SubmissionForm(instance=submission)
    
    context = {'submission': submission, 'form': form, 'assignment': submission.assignment}
    return render(request, 'assignments/edit.html', context)


# ==================== TEACHER GRADE ====================
@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.user.role != 'teacher' or submission.assignment.course.teacher != request.user:
        messages.error(request, "You are not allowed to grade this submission.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        marks = request.POST.get('marks_obtained')
        feedback = request.POST.get('feedback')
        if marks:
            try:
                submission.marks_obtained = float(marks)
                submission.feedback = feedback
                submission.save()
                messages.success(request, "Grade saved.")
            except ValueError:
                messages.error(request, "Invalid marks.")
        else:
            messages.error(request, "Please enter marks.")
        return redirect('dashboard')
    
    context = {
        'submission': submission,
        'assignment': submission.assignment,
        'student': submission.student,
    }
    return render(request, 'assignments/grade.html', context)


# ==================== TEACHER CREATE ASSIGNMENT ====================
@login_required
def create_assignment(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can create assignments.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, teacher=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = form.cleaned_data['course']
            assignment.save()
            messages.success(request, "Assignment created successfully.")
            return redirect('dashboard')
    else:
        form = AssignmentForm(teacher=request.user)
    
    return render(request, 'assignments/create_assignment.html', {'form': form})