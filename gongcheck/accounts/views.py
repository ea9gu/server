# from django.contrib.auth import login
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.views import LoginView
# from django.views.generic.edit import CreateView
# from .forms import CustomUserCreationForm


# class CustomLoginView(LoginView):
#     form_class = AuthenticationForm
#     template_name = 'accounts/login.html'


# class CustomSignupView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'accounts/signup.html'
#     success_url = '/'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return super().form_valid(form)
