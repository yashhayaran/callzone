from django import forms
from .models import UserBase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta(UserBase.Meta):
        model = UserBase
        fields = ["username", "company_name", "email", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]
