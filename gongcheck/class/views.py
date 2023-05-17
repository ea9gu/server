from django.shortcuts import render
from django.http import JsonResponse
from .models import Course, StudentCourse
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

import csv
from io import StringIO
import json

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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StudentCourse

@api_view(['POST'])
@csrf_exempt
def send_signal_to_flutter(request):
    class_id = request.data.get('class_id')
    
    student_ids = StudentCourse.objects.filter(course_id=class_id).values_list('student_id', flat=True)
    
    # TODO: 플러터 앱에 신호를 보내는 코드 추가
    
    return Response({'status': 'success'})
