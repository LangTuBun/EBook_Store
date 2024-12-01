from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Reviews
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
# Create your views here.
books  = [
    "'1': 'The Great Gatsby'",
    "'2': 'The Catcher in the Rye'",
   " '3': 'To Kill a Mockingbird'",
]
def home(request):

    return render(request, 'myapp/home.html')

def employee(request):
    return render(request, 'myapp/employee_home.html')

def user_home(request): 
    return render(request, 'myapp/user_home.html')
    
    
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
    def get_queryset(self):
        return super().get_queryset().prefetch_related('reviews_set')

class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add reviews related to the book to the context
        # context['img_url']= self.object.image.url
        context['reviews'] = Reviews.objects.filter(book=self.object)
        return context
