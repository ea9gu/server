from django.urls import path, include
from . import views

app_name = 'accounts'


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    # path('signup/', include('dj_rest_auth.registration.urls')),
    path('signup/', views.signup, name='signup'),
    path('mylogin/', views.login_view, name='login_view'),
    path('view_user_info/', views.view_user_info, name='view_user_info'),
]