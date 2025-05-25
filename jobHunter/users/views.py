from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "registration/login.html", {})


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration/signup.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "registration/signup.html")
        if re.search("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password) is None:
            messages.error(request, "Password must have at least one letter, one digit, and minimum 8 characters total.")
            return render(request, "registration/signup.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, "registration/signup.html")
    
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return render(request, "registration/signup.html")
    return render(request, "registration/signup.html")
