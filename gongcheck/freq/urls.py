from django.urls import path, include
from . import views

# app_name = 'freq'

urlpatterns = [
    path('generate-freq/', views.generate_freq, name='generate_freq'),
    path('save-attendance/', views.save_attendance, name='save_attendance'),
]
