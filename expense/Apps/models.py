from django.contrib.auth.models import User
from django.db import models

class MonthlyIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_incomes')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"Income for {self.month}/{self.year}: ${self.amount}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    monthly_income = models.ForeignKey(MonthlyIncome, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - ${self.amount} on {self.date} at {self.time}"