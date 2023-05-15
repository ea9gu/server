from django.urls import path, include

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/student/', include('dj_rest_auth.registration.urls')),
    path('signup/professor/', include('dj_rest_auth.registration.urls')),
]