from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from .forms import SignUpForm
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.http import JsonResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def view_user_info(request):
    users = User.objects.all()  # 모든 사용자 가져오기
    return render(request, 'user_info.html', {'users': users})

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            flag = form.cleaned_data['flag']
            password = form.cleaned_data['password1']

            user = User.objects.create_user(username=username, password=password, name=name, flag=flag)
            user.name = name
            user.flag = flag
            user.save()

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # # 토큰을 쿠키에 저장
            # response = redirect('home')
            # response.set_cookie(key='jwt', value=token, httponly=True)

            return redirect('/user/account/view_user_info/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
    else:
        form = AuthenticationForm()
    return JsonResponse({'status': 'fail'})