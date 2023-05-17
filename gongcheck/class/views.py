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
def create_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_name = data.get('course_name')
        professor_id = data.get('professor_id')

        if not course_name:
            return JsonResponse({'status': 'error', 'message': '수업 이름이 제공되지 않았습니다.'})

        # 가장 마지막 번호로 course_id 생성
        last_course = Course.objects.last()
        if last_course:
            last_course_id = int(last_course.course_id)
            course_id = str(last_course_id + 1)
        else:
            course_id = '1'

        # Course 생성
        course = Course(course_id=course_id, name=course_name, professor_id=professor_id)
        course.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})


@csrf_exempt
def enroll_students(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        csv_file = request.FILES['csv_file']

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
                    StudentCourse.objects.get(student_id=user.username, course_id=course_id)
                    students_not_found.append(student_id)
                except ObjectDoesNotExist:
                    course = Course.objects.get(course_id=course_id)
                    student_course = StudentCourse(student_id=user.username, course_id=course.course_id)
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
