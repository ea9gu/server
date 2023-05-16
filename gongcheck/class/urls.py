from django.urls import path, include
from . import views

app_name = 'class'

urlpatterns = [
    path('create-course/', views.create_course, name='create_course'),
    path('enroll-students/', views.enroll_students, name='enroll_students'),
]