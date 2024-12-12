from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_management, name='inventory_management'),
    path('order_books/', views.order_books, name='order_books'),
]
