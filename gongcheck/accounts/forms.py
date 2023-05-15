# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    name = forms.CharField(max_length=255)
    flag = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2', 'flag')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, name=self.cleaned_data['name'], flag=self.cleaned_data['flag'])
        return user
