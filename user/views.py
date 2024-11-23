from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from myapp.models import User, Customer 
from django.db import connection
from .forms import RegistrationForm, LoginForm
from myapp.backends  import CustomRoleBackend
from django.contrib.auth import authenticate


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            registered_date = '2024-11-22' # Set the registered_date to a future date
            
            # Call the add_user method from the custom backend
            custom_backend = CustomRoleBackend()
            new_user = custom_backend.add_user(
                user_name=user_name,    
                first_name=first_name,
                last_name=last_name,
                address=address,
                password=password,
                registered_date=registered_date
            )
            
            if new_user:
                messages.success(request, "Account created successfully")
                return redirect('login')  # Redirect to login page after successful registration
            else:
                messages.error(request, "An error occurred during registration")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                messages.success(request, "Login successful")
                if user.is_employee:
                    return redirect('employee-home')
                else:
                    return redirect('test-home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid form submission")
    else: 
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def profile(request):

    return render(request, 'user/profile.html')

