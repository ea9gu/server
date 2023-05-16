from django.shortcuts import render
from django.http import JsonResponse
from .models import Course

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





