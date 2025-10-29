# expenses/models.py
from django.db import models
from django.utils import timezone

class Expense(models.Model):
    title = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=timezone.now)
    is_cleared = models.BooleanField(default=False)  # like "completed"
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # always return a string (not tuple)
        return f"{self.title} - {self.amount}"

