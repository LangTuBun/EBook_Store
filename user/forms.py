from django import forms
# from django.contrib.auth.models import User
from myapp.models import Customer, Employee, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView,LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django import forms
from myapp.models import User, Customer
class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


    
class LogOutView_(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options', 'trace']    
    def get(self, request, *args, **kwargs):
        logout(request)  # This logs out the user
        return redirect(reverse('test-home'))  # Redirect to the homepage or another page after logout


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Both fields are required.")
        
        return cleaned_data


