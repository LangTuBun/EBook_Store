from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, you are now able to login')
            return redirect('login')
        else:
            messages.error(request, 'Error')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})
@login_required
def profile(request):

    return render(request, 'user/profile.html')