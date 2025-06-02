from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def home(request):
    return render(request, 'pages/home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                messages.success(request, 'Login successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
        
        return redirect('login')
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        my_user = User.objects.create_user(username=username, email=email, password=password1)
        my_user.save()
        messages.success(request, 'User created successfully')
        return redirect('login')
    return render(request, 'auth/register.html')

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('login')
    return render(request, 'pages/home.html')

from django.conf import settings  # Import settings to access EMAIL_HOST_USER

# def forgetpass(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         print("Email : ", email)
#         if User.objects.filter(email=email).exists():
#             user = User.objects.filter(email=email)
#             print(f"User : {user}")
#             send_mail("Reset Your Password : ", f"Current User : {user}", settings.EMAIL_HOST_USER, [email], fail_silently=True)  # Use settings.EMAIL_HOST_USER
#         return redirect('forgetpass')
#     return render(request, 'auth/forgetpass.html')
    