from django.shortcuts import render
from .models import Book

def inventory_management(request):
    books = Book.objects.all()
    return render(request, 'employee_home.html', {'books': books})

def order_books(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        quantity = int(request.POST.get('quantity'))
        
    
        
    books = Book.objects.all()
    return render(request, 'employee_home.html', {'books': books})
