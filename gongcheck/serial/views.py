from django.shortcuts import render
from django.http import JsonResponse
from .models import Device
import json
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_device(request):
    if request.method == 'POST':
        # 프론트에서 전달된 데이터 받기
        data = json.loads(request.body)
        student_id = data.get('student_id')
        device_name = data.get('device_name')
        device_serial = data.get('device_serial')

        # Device 모델에서 같은 device_name을 가진 최근의 데이터 찾기
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=2)
        recent_device = Device.objects.filter(student_id=student_id, timestamp__gte=two_weeks_ago).first()

        # 만약 최근 2주 내에 같은 이름의 디바이스가 등록되었다면, 에러 메시지 반환
        if recent_device:
            response_data = {
                'status': 'error',
                'message': '이미 등록된 디바이스입니다.',
                'device_id': recent_device.id,
                'device_name': recent_device.device_name,
                'timestamp': recent_device.timestamp
            }
            return JsonResponse(response_data)
        
        # Device 모델에 데이터 저장
        device = Device.objects.create(
            student_id=student_id,
            device_name=device_name,
            device_serial=device_serial
        )

        # 현재 저장된 Device 출력
        devices = Device.objects.all().values()
        device_list = list(devices)
        print(device_list)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})

@csrf_exempt
def get_device(request):
    if request.method == 'POST':
        # 프론트에서 전달된 데이터 받기
        data = json.loads(request.body)
        student_id = data.get('student_id')

        # Device 모델에서 같은 device_name을 가진 최근의 데이터 찾기
        recent_device = Device.objects.filter(student_id=student_id).first()

        # 디바이스 정보가 있다면 반환
        if recent_device:
            response_data = {
                'status': 'success',
                'message': '등록된 디바이스가 있습니다',
                'device_id': recent_device.id,
                'device_name': recent_device.device_name,
                'timestamp': recent_device.timestamp
            }
            return JsonResponse(response_data)
        else: return JsonResponse({'status': 'error', 'message': '등록된 디바이스가 없습니다.'})

    return JsonResponse({'status': 'error', 'message': 'POST 요청이 아닙니다.'})
