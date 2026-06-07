from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('edit/<int:submission_id>/', views.edit_submission, name='edit_submission'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('create/', views.create_assignment, name='create_assignment'),
]