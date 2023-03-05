from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import RegisterForm, LoginForm

import json, requests

User = get_user_model()

@login_required
def index(request):
    return render(request, "mony/index.html")

def login_view(request):
    #check if user is already logged in
    if request.user.is_authenticated:
        return redirect('mony:index')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            if (email := form.cleaned_data.get('email')) and (password := form.cleaned_data.get('password')):
                user = authenticate(username=email, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect("mony:index")
                else:
                    messages.add_message(request, messages.ERROR, "Invalid credentials")

    else:
        form = LoginForm
    return render(request, "mony/login.html", {
        "form": form
    })

def logout_view(request):
    logout(request)
    return redirect('mony:login')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if (
                (email := form.cleaned_data.get("email")) and 
                (password := form.cleaned_data.get('password')) and 
                (password_confirmation := form.cleaned_data.get('password_confirmation')) and 
                (first_name := form.cleaned_data.get('first_name')) and 
                (last_name := form.cleaned_data.get('last_name'))
            ):
                if password == password_confirmation:
                    try:
                        user = User.objects.create_user(email, email, password)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()
                        login(request, user)
                        
                    except Exception as e:
                        print(e)
                        messages.add_message(request, messages.ERROR, "Couldn't register user")                    
                    return redirect('mony:index')
                else:
                    messages.add_message(request, messages.ERROR, "Passwords don't match")
    else:
        form = RegisterForm()

    return render(request, "mony/register.html", {
        "form": form
    })
