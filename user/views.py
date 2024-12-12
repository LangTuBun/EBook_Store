from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .models import Profile
from myapp.models import User, Customer
from django.db import connection
from .forms import RegistrationForm, LoginForm
from myapp.backends  import CustomRoleBackend
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            registered_date = '2025-11-23' # Set the registered_date to a future date
            
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
                messages.error(request, "An error occurred during registration (Username may already exist)")
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
                try:
                    request.session['account_id'] = user.account_id
                    request.session['user_name'] = user.user_name
                except Exception as e:
                    print(e)
                if user.from_employee:
                    return redirect('employee-home')
                else:
                    return redirect('user-home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid form submission")
    else: 
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def profile(request):
    user_id = request.session.get('account_id')
    if not user_id:
        messages.error(request, 'Please log in to view your profile.')
        return redirect('login')
    user = User.objects.get(pk=user_id)
    return render(request, 'user/profile.html', {'user': user})


