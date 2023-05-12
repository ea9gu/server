from django.urls import path, include
from . import views

# app_name = 'freq'

urlpatterns = [
    path('generate-freq/', views.generate_freq, name='generate_freq'),
    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.
]
