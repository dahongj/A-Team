from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(strip=True,max_length=50)
    last_name = forms.CharField(strip=True,max_length=50)
    points = 0
    
    class Meta:
        model = CustomUser
        fields = ["email","first_name","last_name"]

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["email","first_name","last_name"]
