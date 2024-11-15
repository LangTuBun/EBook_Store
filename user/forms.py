from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
# Compare this snippet from myapp/views.py:

    
class LogOutView_(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options', 'trace']    
    def get(self, request, *args, **kwargs):
        logout(request)  # This logs out the user
        return redirect(reverse('test-home'))  # Redirect to the homepage or another page after logout