from django.shortcuts import render

# Create your views here.
# 1) def get api(request) : GET요청이 들어오면 Post모델 데이터를 직렬화하여 JSON/XML로 응답하는 함수입니다. 
# 2) def post_api(request) : POST요청이 들어오면 요청 데이터를 Serializer를 사용해 객체화하여 DB에 담는 함수입니다. 

from django.http import JsonResponse
from pydub import AudioSegment
import numpy as np
from .models import AudioFile

def generate_freq(request):
    frequency = int(request.GET.get('frequency', 18000))  # 기본 주파수는 18kHz로 설정
    course_id = int(request.GET.get('course_id', 0))
    number = int(request.GET.get('number', 0))

    # 주파수에 해당하는 음성 생성
    duration = 3000  # 음성의 길이 (3초)
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

    # 음성 파일 저장
    file_path = f'media/audio/{frequency}.wav'
    audio.export(file_path, format='wav')

    # 경로를 데이터베이스에 저장
    audio_file = AudioFile.objects.create(
        frequency=frequency,
        file_path=file_path,
        course_id=course_id,
        number=number
    )

    return JsonResponse({'file_url': audio_file.get_file_url()})