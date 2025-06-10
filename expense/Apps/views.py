from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from .models import *
from datetime import date
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    monthly_income = MonthlyIncome.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    context = {
        'monthly_income' : monthly_income,
        'expenses' : expenses
    }
    return render(request, 'pages/home.html', context)

@login_required
def expense(request):
    if request.method == 'POST':
        
        if 'monthlyIncome' in request.POST:
            amount = request.POST.get('monthlyIncome')
            
            today = date.today()
            month = today.month
            year = today.year
            
            MonthlyIncome.objects.update_or_create(
                user=request.user, 
                month=month,
                year=year,
                defaults={'amount': amount}
            )

        elif 'expenseAmount' in request.POST:
            amount = request.POST.get('expenseAmount')         
            category = request.POST.get('expenseCategory')     
            exp_date = request.POST.get('expenseDate')         
            exp_time = request.POST.get('expenseTime')        

            today = date.today()
            income = MonthlyIncome.objects.filter(user=request.user, month=today.month, year=today.year).first()

            if income:
                Expense.objects.create(
                    user=request.user,
                    monthly_income=income,
                    amount=amount,
                    category=category,
                    date=exp_date,
                    time=exp_time
                )

    today = date.today()
    monthly_income = MonthlyIncome.objects.filter(user=request.user, month=today.month, year=today.year).first()
    
    expenses = Expense.objects.filter(monthly_income=monthly_income) if monthly_income else []

    return render(request, 'pages/expense.html', {
        'monthly_income': monthly_income,
        'expenses': expenses
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
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
