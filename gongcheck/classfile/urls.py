from django.urls import path, include
from . import views

app_name = 'classfile'

urlpatterns = [
    # path('create-course/', views.create_course, name='create_course'),
    # path('enroll-students/', views.enroll_students, name='enroll_students'),
    path('create-and-enroll/', views.create_and_enroll, name='create_and_enroll'),
    path('activate-signal/', views.send_signal_to_flutter, name='send_signal_to_flutter'),
    path('student-course/', views.get_student_course, name='get_student_course'),
    path('prof-course/', views.get_prof_course, name='get_prof_course'),
    path('get-attendance-data/', views.get_attendance_data, name='get_attendance_data'),
    path('fix-attendance/', views.fix_attendance, name='fix_attendance'),
]