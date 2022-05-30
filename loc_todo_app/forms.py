from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

from .models import TodoItem



class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class TodoForm(forms.ModelForm):

    class Meta:
        fields = "__all__"

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]