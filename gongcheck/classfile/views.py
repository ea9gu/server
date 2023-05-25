from django.shortcuts import render
from django.http import JsonResponse
from .models import Course, StudentCourse
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

import csv
from io import StringIO
import json

from django.utils import timezone
from datetime import datetime, timedelta
from freq.models import AudioFile, Attendance

from django.shortcuts import get_object_or_404

@csrf_exempt
def create_and_enroll(request):
    if request.method == 'POST':
        # Extract data from the request
        #data = json.loads(request.body)
        course_name =  request.POST.get('course_name')
        professor_id =  request.POST.get('professor_id')
        course_id =  request.POST.get('course_id')
        csv_file = request.FILES.get('csv_file')

        # Check if all required data is provided
        if not course_name or not professor_id or not course_id or not csv_file:
            return JsonResponse({'status': 'error', 'message': '요청 데이터가 부족합니다.'})

        # 새로운 course이면 생성하고, 아니면 기존의 data를 불러오도록 함
        course, created = Course.objects.get_or_create(course_id=course_id, defaults={'name': course_name, 'professor_id': professor_id})

        if not created:
            course.name = course_name
            course.professor_id = professor_id
            course.save()

        # CSV 파일을 문자열로 읽어옴
        csv_data = csv_file.read().decode('utf-8')

        # CSV 데이터를 파싱하여 학생 번호를 추출하고, StudentCourse에 추가
        students_added = []
        students_not_found = []
        csv_reader = csv.reader(StringIO(csv_data))
        for row in csv_reader:
            student_id = row[0]  # 학생 번호가 있는 열을 지정해야 함
            # User 정보 확인
            try:
                user = User.objects.get(username=student_id, flag=0)

                # StudentCourse에 추가하기 전에 중복 여부 확인
                try:
                    StudentCourse.objects.get(student_id=user.username, course_id=course)
                    students_not_found.append(student_id)
                except ObjectDoesNotExist:
                    student_course = StudentCourse(student_id=user.username, course_id=course)
                    student_course.save()
                    students_added.append(student_id)

            except User.DoesNotExist:
                students_not_found.append(student_id)

        response_data = {
            'status': 'success',
            'students_added': students_added,
            'students_not_found': students_not_found
        }
        return JsonResponse(response_data)

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})


@csrf_exempt
def send_signal_to_flutter(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_id = request.POST.get('student_id')

        if not course_id or not student_id:
            return JsonResponse({'status': 'error'})

        # Get the current datetime
        current_datetime = timezone.now()
        activation_duration = timedelta(minutes=5)  # Default activation duration if not found in the database

        try:
            audio_file = AudioFile.objects.filter(course_id=course_id).latest('created_at')
            activation_duration = timedelta(minutes=audio_file.activation_duration)
        except AudioFile.DoesNotExist:
            return JsonResponse({'status': 'bluecheck'})

        # Calculate the datetime threshold (activation_duration minutes ago)
        threshold_datetime = current_datetime - activation_duration

        print(threshold_datetime)
        try:
            latest_audio_file = AudioFile.objects.filter(course_id=course_id, created_at__gte=threshold_datetime).latest('created_at')

            # Check if the latest audio file is within the activation_duration timeframe
            if latest_audio_file.created_at >= threshold_datetime:
                return JsonResponse({'status': 'check'})
            else:
                return JsonResponse({'status': 'bluecheck'})

        except AudioFile.DoesNotExist:
            return JsonResponse({'status': 'bluecheck'})

    return JsonResponse({'status': 'error'})

### 학생의 과목 출력
@csrf_exempt
def get_student_course(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')

        if student_id is not None:
            courses = StudentCourse.objects.filter(student_id=student_id)
            course_list = []

            for course in courses:
                course_info = {
                    'course_id': course.course_id.course_id,
                    'name': course.course_id.name
                }
                course_list.append(course_info)

            return JsonResponse({'courses': course_list})
        else:
            return JsonResponse({'error': 'student_id parameter is required.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
### 교수의 과목 출력
@csrf_exempt
def get_prof_course(request):
    if request.method == 'GET':
        professor_id = request.GET.get('professor_id')

        if professor_id is not None:
            courses = Course.objects.filter(professor_id=professor_id)
            course_list = []

            for course in courses:
                course_info = {
                    'course_id': course.course_id,
                    'name': course.name
                }
                course_list.append(course_info)

            return JsonResponse({'courses': course_list})
        else:
            return JsonResponse({'error': 'professor_id parameter is required.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


######## 출석부 출력 코드
@csrf_exempt
def get_attendance_data(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        date = request.POST.get('date') 
        student_id = request.POST.get('student_id')
    else: return JsonResponse({'error': 'Invalid request method.'})

    # 클래스 정보 가져오기
    course = get_object_or_404(Course, course_id=course_id)

    # 학생들의 ID 가져오기
    student_ids = StudentCourse.objects.filter(course_id=course).values_list('student_id', flat=True)

    if date and student_id: 
        attendance_data = Attendance.objects.filter(course_id=course_id, student_id=student_id, date=date).order_by('date')
        if not attendance_data.exists():
            return JsonResponse({'error': 'Attendance data not found for the specified student_id with date.'})
    elif date: 
        attendance_data = Attendance.objects.filter(course_id=course_id, student_id__in=student_ids, date=date).order_by('student_id')
        if not attendance_data.exists(): return JsonResponse({'error': 'Attendance data not found for the specified date.'})
    elif student_id:
        attendance_data = Attendance.objects.filter(course_id=course_id, student_id=student_id).order_by('date')
        if not attendance_data.exists():
            return JsonResponse({'error': 'Attendance data not found for the specified student_id.'})
    else: attendance_data = Attendance.objects.filter(course_id=course_id, student_id__in=student_ids).order_by('date')

    # 날짜별 및 학번별 출석 데이터 구성
    attendance_by_student_and_date = {}

    if date and student_id: 
        for attendance in attendance_data:
            if attendance.student_id not in attendance_by_student_and_date:
                attendance_by_student_and_date[str(attendance.date)] = {}
            attendance_by_student_and_date[str(attendance.date)] = int(attendance.attend)

    elif date:
        for attendance in attendance_data:
            if attendance.student_id not in attendance_by_student_and_date:
                attendance_by_student_and_date[attendance.student_id] = {}
            attendance_by_student_and_date[attendance.student_id] = int(attendance.attend)

    elif student_id: 
        for attendance in attendance_data:
            if attendance.student_id not in attendance_by_student_and_date:
                attendance_by_student_and_date[str(attendance.date)] = {}
            attendance_by_student_and_date[str(attendance.date)] = int(attendance.attend)
            # if attendance.student_id == student_id:
            #     attendance_by_student_and_date[attendance.student_id] = {str(attendance.date): int(attendance.attend)}
        
    else:
        for attendance in attendance_data:
            if attendance.student_id not in attendance_by_student_and_date:
                attendance_by_student_and_date[attendance.student_id] = {}
            attendance_by_student_and_date[attendance.student_id][str(attendance.date)] = int(attendance.attend)

    try:
        student_names = User.objects.filter(username__in=student_ids).values('username', 'name')
        student_names_dict = {student['username']: student['name'] for student in student_names}
        if student_id: student_names_dict = student_names_dict.get(student_id, '')
    except: 
        student_names_dict = {}

    response_data = {
        'course_id': course_id,
        'student_names': student_names_dict,
        'attendance_data': attendance_by_student_and_date,
        'dates': sorted(list(set([str(a.date) for a in attendance_data]))),
    }

    return JsonResponse(response_data)

    # return JsonResponse(attendance_by_student_and_date)

@csrf_exempt
def fix_attendance(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        date = request.POST.get('date')
        student_id = request.POST.get('student_id')
        bef_att = request.POST.get('bef_att')
        aft_att = request.POST.get('aft_att')

        try:
            attendance = Attendance.objects.get(course_id=course_id, date=date, student_id=student_id, attend=(bef_att == 'True'))
            attendance.attend = (aft_att == 'True')
            attendance.save()
            return JsonResponse({'success': 'Attendance fixed successfully.'})

        except Attendance.DoesNotExist:
            return JsonResponse({'error': 'Attendance data not found.'})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
