from django.urls import path
from . import analytics_views

urlpatterns = [
    path('', analytics_views.admin_analytics, name='admin_analytics'),
]