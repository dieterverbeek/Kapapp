# KAPPERAPP/kapperapp/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Gebruikersnaam",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )
    password = forms.CharField(
        label="Wachtwoord",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''})
    )