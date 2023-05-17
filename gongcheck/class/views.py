from django.shortcuts import render
from django.http import JsonResponse
from .models import Course, StudentCourse
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

import csv
from io import StringIO
import json

from datetime import datetime, timedelta
from freq.models import AudioFile

@csrf_exempt
def create_and_enroll(request):
    if request.method == 'POST':
        # Extract data from the request
        data = json.loads(request.body)
        course_name = data.get('course_name')
        professor_id = data.get('professor_id')
        course_id = data.get('course_id')
        csv_file = request.FILES.get('csv_file')

        # Check if all required data is provided
        if not course_name or not professor_id or not course_id or not csv_file:
            return JsonResponse({'status': 'error', 'message': '요청 데이터가 부족합니다.'})

        # Create the course
        course, _ = Course.objects.get_or_create(course_id=course_id, defaults={'name': course_name, 'professor_id': professor_id})

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

@api_view(['POST'])
@csrf_exempt
def send_signal_to_flutter(request):
    if request.method == 'POST':
        class_id = request.data.get('class_id')
        student_id = request.data.get('student_id')

        # Check if both class_id and student_id are provided
        if not class_id or not student_id:
            return Response({'status': 'error'})

        # Get the current datetime
        current_datetime = datetime.now()

        # Calculate the datetime threshold (10 minutes ago)
        threshold_datetime = current_datetime - timedelta(minutes=10)

        try: latest_audio_file = AudioFile.objects.filter(class_id=class_id, student_id=student_id, created_at__gte=threshold_datetime).latest('created_at')

            # Check if the latest audio file is within the 10-minute timeframe
            if latest_audio_file.created_at >= threshold_datetime: return Response({'status': 'check'})
            else: return Response({'status': 'bluecheck'})

        except AudioFile.DoesNotExist: return Response({'status': 'bluecheck'})

    return Response({'status': 'error'})
