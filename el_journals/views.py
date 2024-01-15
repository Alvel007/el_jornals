from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import CustomAuthenticationForm
from django.http import HttpResponse


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect(reverse('op_manual'))
                response['Cache-Control'] = 'no-store'
                return response
    else:
        form = CustomAuthenticationForm()
    return render(request, 'staff/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
