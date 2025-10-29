# expenses/admin.py
from django.contrib import admin
from .models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'is_cleared', 'updated_at')
    search_fields = ('title', 'category')
    list_filter = ('is_cleared', 'category')

admin.site.register(Expense, ExpenseAdmin)
