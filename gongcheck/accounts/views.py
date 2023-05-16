from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserJWTSignupSerializer

class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({'user': serializer.data,
                                 'access': access,
                                 'refresh': refresh})
        else:
            return JsonResponse(serializer.errors, status=400)

from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally, perform additional actions after successful signup
            return redirect('home')  # Replace 'home' with the desired URL
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
