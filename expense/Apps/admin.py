from django.contrib import admin
from .models import *

admin.site.register(MonthlyIncome)  # ✅ Pass the model class, not a string
admin.site.register(Expense)