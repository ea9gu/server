from django.urls import path
from . import views

urlpatterns = [
    path('save-device/', views.save_device, name='save_device'),
    path('get-device/', views.get_device, name='get_device'),
]