from django.shortcuts import render
from django.http import JsonResponse
from .models import Course, StudentCourse
from django.contrib.auth.models import User

import csv
from io import StringIO

def create_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        # 가장 마지막 번호로 course_id 생성
        last_course = Course.objects.last()
        if last_course:
            last_course_id = int(last_course.course_id)
            course_id = str(last_course_id + 1)
        else: course_id = '1'

        # Course 생성
        course = Course(course_id=course_id, name=course_name)
        course.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})



def enroll_students(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        csv_file = request.FILES['csv_file']

        # CSV 파일을 문자열로 읽어옴
        csv_data = csv_file.read().decode('utf-8')
        
        # CSV 데이터를 파싱하여 학생 번호를 추출하고, StudentCourse에 추가
        students_added = []
        csv_reader = csv.reader(StringIO(csv_data))
        for row in csv_reader:
            student_id = row[0]  # 학생 번호가 있는 열을 지정해야 함
            
            # User 정보 확인
            try: user = User.objects.get(username=student_id, flag=0)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'학생 번호 {student_id}에 해당하는 정보가 없거나 유효하지 않습니다.'})
            
            # StudentCourse에 추가
            course = Course.objects.get(course_id=course_id)
            student_course = StudentCourse(student_id=user.username, course_id=course.course_id)
            student_course.save()
            
            students_added.append(student_id)
        
        return JsonResponse({'status': 'success', 'students_added': students_added})
    
    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})


