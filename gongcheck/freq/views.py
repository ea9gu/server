from django.shortcuts import render

# Create your views here.
# 1) def get api(request) : GET요청이 들어오면 Post모델 데이터를 직렬화하여 JSON/XML로 응답하는 함수입니다. 
# 2) def post_api(request) : POST요청이 들어오면 요청 데이터를 Serializer를 사용해 객체화하여 DB에 담는 함수입니다. 
from .models import AudioFile, Attendance
from classfile.models import StudentCourse, Course

from django.http import HttpResponse, JsonResponse
from pydub import AudioSegment
import numpy as np
import os
import json
from scipy.io.wavfile import read
from datetime import datetime, timedelta

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_freq(request):
    frequency = int(request.GET.get('frequency', 20000))  # 기본 주파수는 18kHz로 설정
    course_id = request.GET.get('course_id')
    number = int(request.GET.get('number', 0))
    activation_duration = int(request.GET.get('activation_duration', 5))

    if course_id is None:
        return JsonResponse({'error': 'course_id parameter is missing.'}, status=400)

    # 주파수에 해당하는 음성 생성
    duration = 5000  # 음성의 길이 (5초)
    sample_rate = 44100  # 샘플링 속도
    t = np.linspace(0, duration, int(sample_rate * duration / 1000), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    audio_data = (audio_data * 32767).astype(np.int16)

    # 음성 데이터를 WAV 형식으로 변환
    audio = AudioSegment(
        audio_data.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )

    file_path = f'audio_{frequency}.wav'  # audio_18000.wav
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_path)
    audio.export(file_path, format='wav')

    # 경로를 데이터베이스에 저장
    audio_file = AudioFile.objects.create(
        frequency=frequency,
        file_path=file_path,
        course_id=course_id,
        number=number,
        activation_duration=activation_duration,
    )

    course = Course.objects.get(course_id=course_id)
    student_ids = StudentCourse.objects.filter(course_id=course).values_list('student_id', flat=True)


    # 모든 학생들의 데이터 추가
    date = datetime.date.today()
    for student_id in student_ids:
        Attendance.objects.create(
            student_id=student_id,
            course_id=course_id,
            date=date,
            attend=False,
            course_number=number,
        )

    return JsonResponse({'course_id': course_id, 'file_url': audio_file.get_file_url()})
    # return JsonResponse({'file_url': file_path})
    

@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        # 프론트에서 전달된 데이터 받기
        try: data = json.loads(request.body.decode('utf-8'))
        except UnicodeDecodeError: return JsonResponse({'status': 'error', 'message': '올바른 인코딩 형식이 아닙니다.'})

        student_id = data.get('student_id')
        course_id = data.get('course_id')
        date = data.get('date')
        attend = 0 # 기본값은 미출석 처리
        audio_file = request.FILES.get('recording')

        latest_attendance = Attendance.objects.filter(course_id=course_id).order_by('-course_number').first()
        if latest_attendance: course_number = latest_attendance.course_number + 1
        else: course_number = 1

        current_datetime = datetime.now()
        activation_duration = timedelta(minutes=5)  # Default activation duration if not found in the database

        try:
            audio_file = AudioFile.objects.filter(course_id=course_id).latest('created_at')
            activation_duration = timedelta(minutes=audio_file.activation_duration)
        except AudioFile.DoesNotExist:
            return JsonResponse({'status': 'error'})

        # Calculate the datetime threshold (activation_duration minutes ago)
        threshold_datetime = current_datetime - activation_duration
        
        try:
            latest_audio_file = AudioFile.objects.filter(course_id=course_id, created_at__gte=threshold_datetime).latest('created_at')

            # Check if the latest audio file is within the activation_duration timeframe
            if latest_audio_file.created_at >= threshold_datetime: pass
            else: return JsonResponse({'status': 'error'})
        except: return JsonResponse({'status': 'error'})
        
        if audio_file:
            # 음성 녹음 파일을 저장하고 파일 경로를 얻습니다.
            file_name = 'record.wav'
            recording_path = os.path.join(os.getcwd(), file_name)
            with open(recording_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # 주파수 분석을 수행합니다.
            sample_rate, data = read(recording_path)
            # data를 활용하여 주파수 분석 및 처리를 수행합니다.

            # 주파수 값과 일치하는 AudioFile을 찾습니다.
            try:
                audio = AudioFile.objects.get(frequency=data)
                # attendance.attend = 1  # 출석 처리
                # attendance.save()
                # Update the attend field of specific records in the database
                Attendance.objects.filter(student_id=student_id, course_id=course_id, attend=0).update(attend=1)
                return JsonResponse({'status': 'success', 'message': '출석 처리 완료'})
            except AudioFile.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '주파수 값과 일치하는 오디오 파일이 없습니다.'})

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})
