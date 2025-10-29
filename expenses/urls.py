# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('clear/<int:pk>/', views.mark_as_cleared, name='mark_as_cleared'),
    path('unclear/<int:pk>/', views.mark_as_uncleared, name='mark_as_uncleared'),
]
