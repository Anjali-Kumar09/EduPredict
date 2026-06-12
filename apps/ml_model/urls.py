from django.urls import path
from . import views

urlpatterns = [
    path('predict/<int:student_id>/', views.predict_student, name='predict_student'),
    path('batch-predict/', views.batch_predict_csv, name='batch_predict'),   # <-- this line
]