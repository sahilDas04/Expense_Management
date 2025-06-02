from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import *
from datetime import date
import calendar
from django.db.models import Sum


def home(request):
    today = date.today()
    monthly_income = MonthlyIncome.objects.filter(month=today.month, year=today.year).first()
    expenses = Expense.objects.filter(monthly_income=monthly_income) if monthly_income else []

    # Monthly data for pie chart
    monthly_data = Expense.objects.values('monthly_income__month').annotate(total=Sum('amount')).order_by('monthly_income__month')
    month_labels = [calendar.month_abbr[item['monthly_income__month']] for item in monthly_data]
    month_totals = [float(item['total']) for item in monthly_data]

    # Daily data for bar chart
    daily_data = Expense.objects.filter(monthly_income=monthly_income).values('date').annotate(total=Sum('amount')).order_by('date')
    day_labels = [item['date'].strftime('%d %b') for item in daily_data]
    day_totals = [float(item['total']) for item in daily_data]

    return render(request, 'pages/home.html', {
        'monthly_income': monthly_income,
        'expenses': expenses,
        'month_labels': month_labels,
        'month_totals': month_totals,
        'day_labels': day_labels,
        'day_totals': day_totals
    })

def expense(request):
    # When the form is submitted
    if request.method == 'POST':
        
        # Check if the Monthly Income form was submitted
        if 'monthlyIncome' in request.POST:
            amount = request.POST.get('monthlyIncome')  # Get the income amount from the form
            
            # Get the current month and year
            today = date.today()
            month = today.month
            year = today.year
            
            # Update the income if exists, or create a new record for the current month and year
            MonthlyIncome.objects.update_or_create(
                month=month, year=year,
                defaults={'amount': amount}
            )

        # Check if the Expense form was submitted
        elif 'expenseAmount' in request.POST:
            amount = request.POST.get('expenseAmount')          # Get expense amount
            category = request.POST.get('expenseCategory')      # Get expense category
            exp_date = request.POST.get('expenseDate')          # Get expense date
            exp_time = request.POST.get('expenseTime')          # Get expense time

            # Find the current month's income record to link the expense to it
            today = date.today()
            income = MonthlyIncome.objects.filter(month=today.month, year=today.year).first()

            # If there is a monthly income recorded, save the expense
            if income:
                Expense.objects.create(
                    monthly_income=income,
                    amount=amount,
                    category=category,
                    date=exp_date,
                    time=exp_time
                )

    # For displaying data on the page:
    today = date.today()
    monthly_income = MonthlyIncome.objects.filter(month=today.month, year=today.year).first()
    
    # Get all expenses linked to this month's income
    expenses = Expense.objects.filter(monthly_income=monthly_income) if monthly_income else []

    # Pass data to the template
    return render(request, 'pages/expense.html', {
        'monthly_income': monthly_income,
        'expenses': expenses
    })

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
