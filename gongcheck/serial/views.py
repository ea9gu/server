from django.shortcuts import render
from django.http import JsonResponse
from .models import Device
from datetime import datetime, timedelta
import json

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_device(request):
    if request.method == 'POST':
        # 프론트에서 전달된 데이터 받기
        data = json.loads(request.body)
        device_name = data.get('device_name')
        device_serial = data.get('device_serial')
        student_id = data.get('student_id')

        # Device 모델에서 같은 device_name을 가진 최근의 데이터 찾기
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        recent_device = Device.objects.filter(student_id=student_id, timestamp__gte=two_weeks_ago).first()

        # 만약 최근 2주 내에 같은 이름의 디바이스가 등록되었다면, 에러 메시지 반환
        if recent_device:
            return JsonResponse({'status': 'error', 'message': '이미 등록된 디바이스입니다.'})

        # Device 모델에 데이터 저장
        device = Device.objects.create(
            device_name=device_name,
            device_serial=device_serial,
            student_id=student_id
        )

        # 현재 저장된 Device 출력
        devices = Device.objects.all().values()
        device_list = list(devices)
        print(device_list)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})
