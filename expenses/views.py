# expenses/views.py
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Expense

def home(request):
    """
    Home view with optional filter (all / month / year).
    - filter is taken from ?filter=all|month|year
    - calculates pending, cleared, totals and provides a motivational message
    """
    # read filter from query parameter (default = all)
    filter_option = request.GET.get('filter', 'all')
    today = date.today()

    # build base queryset according to filter
    if filter_option == 'month':
        base_qs = Expense.objects.filter(date__year=today.year, date__month=today.month)
    elif filter_option == 'year':
        base_qs = Expense.objects.filter(date__year=today.year)
    else:
        base_qs = Expense.objects.all()

    # Separate pending (uncleared) and cleared
    expenses = base_qs.filter(is_cleared=False).order_by('-updated_at')
    cleared_expenses = base_qs.filter(is_cleared=True).order_by('-updated_at')

    # Totals
    pending_total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    cleared_total = cleared_expenses.aggregate(total=Sum('amount'))['total'] or 0

    # total_spent = cleared_total (money already spent/cleared)
    total_spent = cleared_total

    # overall total for the selected filter (sum of all amounts in base_qs)
    overall_total = base_qs.aggregate(total=Sum('amount'))['total'] or 0


    context = {
        'expenses': expenses,
        'cleared_expenses': cleared_expenses,
        'pending_total': pending_total,
        'cleared_total': cleared_total,
        'total_spent': total_spent,
        'overall_total': overall_total,
        'filter_option': filter_option,
        
    }
    return render(request, 'expenses/home.html', context)


def add_expense(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        amount = request.POST.get('amount', '0').strip() or '0'
        category = request.POST.get('category', '').strip()
        date_val = request.POST.get('date', None)
        description = request.POST.get('description', '').strip()
        Expense.objects.create(
            title=title,
            amount=amount,
            category=category,
            date=date_val if date_val else None,
            description=description
        )
    return redirect('home')


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.title = request.POST.get('title', expense.title)
        expense.amount = request.POST.get('amount', expense.amount)
        expense.category = request.POST.get('category', expense.category)
        expense.date = request.POST.get('date', expense.date)
        expense.description = request.POST.get('description', expense.description)
        expense.save()
        return redirect('home')
    return render(request, 'expenses/edit_expense.html', {'expense': expense})


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('home')


def mark_as_cleared(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.is_cleared = True
    expense.save()
    return redirect('home')


def mark_as_uncleared(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.is_cleared = False
    expense.save()
    return redirect('home')
