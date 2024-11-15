from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.views.generic import ListView, DetailView

# Create your views here.
books  = [
    "'1': 'The Great Gatsby'",
    "'2': 'The Catcher in the Rye'",
   " '3': 'To Kill a Mockingbird'",
]
def home(request):

    return render(request, 'myapp/home.html')



    
    
def order(request):
    book_names = {
        'books': Book.objects.all(),
        'title': 'Order'
    }   
    return render(request , 'myapp/order.html',book_names )

class BookListView(ListView):
    model = Book
    template_name = 'myapp/order.html'
    context_object_name = 'books'
    ordering = ['publishdate']   
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'
