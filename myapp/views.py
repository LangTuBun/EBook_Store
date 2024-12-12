from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Book, Reviews, CartItem, Customer, User, Category, Orders, OrderDetail, Employee
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch, Max
from django.contrib import messages
from datetime import datetime, timedelta    
from django.db import Error
# Create your views here.

def home(request):
    book_names = {
    'books': Book.objects.all()
}   
    return render(request, 'myapp/home.html', book_names)

def employee(request):
    book_names = {
    'books': Book.objects.all()
    }   
    return render(request, 'myapp/employee_home.html', book_names)

def user_home(request): 
    return render(request, 'myapp/user_home_main.html')
    
    
def order(request):
    book_names = {
        'books': Book.objects.all(),
        'title': 'Order'
    }   
    return render(request , 'myapp/order.html',book_names )

def user_order(request):    
    # Get all books
    books = Book.objects.all().prefetch_related('reviews_set')

    # Get all categories
    categories = Category.objects.all()

    # Get the selected category from query parameters
    selected_category = request.GET.get('category', None)
    sort_option = request.GET.get('sort', None)
    
    # Filter books if a category is selected
    if selected_category:
        books = books.filter(category_id__icontains=selected_category)
    if sort_option == "alphabet":
        books = books.order_by('title')  # Sort alphabetically
    elif sort_option =="alphabetZ-A":
        books = books.order_by('-title')
    elif sort_option == "price_asc":
        books = books.order_by('price')  # Sort by price (ascending)
    elif sort_option == "price_desc":
        books = books.order_by('-price')  # Sort by price (descending)

    # Render the template with books and categories
    return render(request, 'myapp/user_order.html', {
        'books': books,
        'categories': categories,
        'selected_category': selected_category,
        'sort_option': sort_option
    })


class BookListView(ListView):
    model = Book
    template_name = 'myapp/order.html'
    context_object_name = 'books'
    ordering = ['publishdate']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('reviews_set')
        category = self.request.GET.get('category', None)  # Get the category from query parameters
        if category:
            queryset = queryset.filter(category__name=category)  # Filter by category
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass all categories to the template
        context['selected_category'] = self.request.GET.get('category', None)  # Include the selected category
        return context
    
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add reviews related to the book to the context
        context['reviews'] = Reviews.objects.filter(book=self.object)

        # Add categories related to the book to the context
        category_ids = [int(cid) for cid in self.object.category_id.split(',')]
        categories = Category.objects.filter(category_id__in=category_ids)  # Use 'category_id' here
        context['categories'] = categories

        return context

    
    



class UserBookDetailView(DetailView):
    model = Book
    template_name = 'myapp/user_book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add reviews related to the book to the context
        context['reviews'] = Reviews.objects.filter(book=self.object)

        # Add categories related to the book to the context
        category_ids = [int(cid) for cid in self.object.category_id.split(',')]
        categories = Category.objects.filter(category_id__in=category_ids)  # Use 'category_id' here
        context['categories'] = categories

        return context
    
def add_to_cart(request, pk):
    if request.method == 'POST':
        # Retrieve user_id from session (or your desired source)
        user_id = request.session.get('account_id') 
        if not user_id:
            return HttpResponse('You must be logged in to add to the cart.', status=403)

        user = User.objects.get(pk=user_id)

        # Get the Book instance
        book = get_object_or_404(Book, pk=pk)

        # Get the quantity from the form (default to 1 if not provided or invalid)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                raise ValueError  # Ensure quantity is at least 1
        except ValueError:
            return HttpResponse('Invalid quantity value.', status=400)

        # Create or update the CartItem
        cart_item, created = CartItem.objects.get_or_create(
            user_id=user,  # Assign the User instance
            book_id=book,  # Provide the Book instance
            defaults={'quantity': quantity}  # Defaults for new CartItem
        )

        if not created:
            # Increment the quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, "Book added to cart successfully.")
        return redirect('user-book-detail', pk=pk)



def Cart(request):
    user_id = request.session.get('account_id')
    if not user_id:
        messages.error(request, 'Please log in to view your cart.')
        return redirect('login')
    user = User.objects.get(pk=user_id)
    cart_items = CartItem.objects.filter(user_id=user)
    
    total = sum(item.get_total_price() for item in cart_items)
    
    return render(request, 'myapp/user_cart.html', {
        'cart_items': cart_items,
        'total': total
    })
def remove_from_cart(request, cart_item_id):
    # Verify the user is logged in
    user_id = request.session.get('account_id')
    if not user_id:
        messages.error(request, 'Please log in to manage your cart.')
        return redirect('login')  # Redirect to login page

    try:
    
        cart_item = CartItem.objects.get(
            id=cart_item_id, 
            user_id_id=user_id  
        )
        
        # Delete the cart item
        cart_item.delete()
        
        # Add a success message
        messages.success(request, 'Item removed from cart successfully.')
    
    except CartItem.DoesNotExist:
        # Handle case where cart item is not found
        messages.error(request, 'Cart item not found.')
    
    # Redirect back to the cart page
    return redirect('cart')



def generate_new_order_id():
    # Get the latest order_id
    last_order = Orders.objects.all().aggregate(Max('order_id'))
    last_order_id = last_order['order_id__max']

    if last_order_id is not None:
        # Increment the last order_id by 1
        new_order_id = last_order_id + 1
    else:
        # If there are no previous orders, start with order_id 1
        new_order_id = 1

    return new_order_id
def generate_new_order_detail_id():
    # Get the latest order_id
    last_order = OrderDetail.objects.all().aggregate(Max('order_detail_id'))
    last_order_id = last_order['order_detail_id__max']

    if last_order_id is not None:
        # Increment the last order_id by 1
        new_order_id = last_order_id + 1
    else:
        # If there are no previous orders, start with order_id 1
        new_order_id = 1

    return new_order_id

def checkout(request):
    user_id = request.session.get('account_id')
    user = User.objects.get(pk=user_id)
    cart_items = CartItem.objects.filter(user_id=user)
    
    # Get customer instance
    customer_id = Customer.objects.get(account_id=user).customer_id
    
    # Calculate the total price for all items in the cart
    total_price = sum(item.get_total_price() for item in cart_items)
    new_order_id = generate_new_order_id()
    # Create a new Order instance for the customer
    order = Orders.objects.create(
        order_id=new_order_id,
        customer_id=customer_id, 
        order_date=datetime.now(),
        shipped_date=datetime.now() + timedelta(days=7),
        from_employee=0,  # Assuming 0 means a regular customer order
        status = 'Pending'
    )

    # Create OrderDetail instances for each item in the cart
    for cart_item in cart_items:
        new_order_detail_id = generate_new_order_detail_id()
        OrderDetail.objects.create(
            order_detail_id = new_order_detail_id,
            order_id=order.order_id,  # Link this detail to the newly created order
            book_id=cart_item.book_id.book_id,
            quantity=cart_item.quantity,
            price_each=cart_item.book_id.price
        )

        

    # Clear the cart after the order is placed
    cart_items.delete()

    # Redirect the user to an order confirmation page or similar
    order_details = OrderDetail.objects.filter(order_id=order)
    
    # Render the confirmation page with the order details
    return render(request, 'myapp/user_order_confirmation.html', {
        'order': order,
        'order_details': order_details,
        'total_price': total_price
    })


def order_history(request):
    user_id = request.session.get('account_id')
    if not user_id:
        messages.error(request, 'Please log in to view your order history.')
        return redirect('login')  # Redirect to login page
    user = User.objects.get(pk=user_id)
    customer_id = Customer.objects.get(account_id=user).customer_id
    orders = Orders.objects.filter(customer_id=customer_id)
    return render(request, 'myapp/user_order_history.html', {'orders': orders})

def history_detail(request, pk):
    order = Orders.objects.get(order_id=pk)
    order_details = OrderDetail.objects.filter(order_id=order)
    total_price = sum(detail.get_total_price() for detail in order_details) 
    return render(request, 'myapp/user_order_confirmation.html', {
        'order': order,
        'order_details': order_details,
        'total_price': total_price
    })
    
def dashboard(request):
    low_stock = Book.objects.filter(amount__lte=25)   
    pending_orders = Orders.objects.filter(status='Pending')    
    return render(request, 'myapp/employee_dashboard.html', {
        'lowstock': low_stock,
        'pending_orders': pending_orders
    })
    

def employee_orders(request):
    pass

def employee_process_orders(request,pk):
    order = Orders.objects.get(order_id=pk)
    order_details = OrderDetail.objects.filter(order_id=order)
    total_price = sum(detail.get_total_price() for detail in order_details)
    if request.method == 'POST':
        for detail in order_details:
            book = Book.objects.get(book_id=detail.book.book_id)
            if book.amount < detail.quantity:
                messages.error(request, f'Not enough stock for {book.title}.')
                return redirect('employee-order-processing', pk=pk)
            book.amount -= detail.quantity
            book.save()
        order.status = 'Shipped'
        order.save()
        return redirect('employee-dashboard')
    return render(request, 'myapp/employee_process_order.html', {
        'order': order,
        'order_details': order_details,
        'total_price': total_price
    })
    
def restock_books(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
            if amount < 1:
                raise ValueError
        except ValueError:
            messages.error(request, 'Invalid amount value.')
            return redirect('employee-dashboard')
        book.amount += amount
        book.save()
        messages.success(request, f'{book.title} Restock request sent to publisher successfully.')
        employee_id_ = request.session.get('account_id')
        employee_id_real = Employee.objects.get(account_id=employee_id_).employee_id
        new_order_detail_id = generate_new_order_detail_id()
        order = Orders.objects.create(
            order_id=generate_new_order_id(),
            employee_id=employee_id_real,  # Assuming 1 is the publisher's customer_id
            order_date=datetime.now(),
            shipped_date=datetime.now() + timedelta(days=7),
            from_employee=1,  # Assuming 1 means an employee order
            status='Shipped'
        )
        OrderDetail.objects.create(
            order_detail_id=new_order_detail_id,
            order_id=order.order_id,
            book_id=book.book_id,
            quantity=amount,
            price_each=book.price
        )
        return redirect('employee-dashboard')
    return render(request, 'myapp/restock_book.html', {'book': book})
    

def inventory(request):
    sort_by = request.GET.get('sort', 'title')
    order = request.GET.get('order', 'asc')
    
    if sort_by == 'title':
        books = Book.objects.all().order_by('title' if order == 'asc' else '-title')
    elif sort_by == 'amount':
        books = Book.objects.all().order_by('amount' if order == 'asc' else '-amount')
    else:
        books = Book.objects.all().order_by('title')
    
    return render(request, 'myapp/inventory_management.html', {'books': books})

def update_book(request,pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        price = request.POST.get('price')
        amount = request.POST.get('amount')
        publishdate = request.POST.get('publishdate')
        book.price = price
        book.amount = amount
        book.publishdate = publishdate
        book.save()
        messages.success(request, 'Book updated successfully.')
        return redirect('inventory-management')
    return render(request, 'myapp/update_book.html', {'book': book}) 

def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('inventory-management')

def order_history_employee(request):
    user_id = request.session.get('account_id')
    user = User.objects.get(pk=user_id)
    employee_id_real = Employee.objects.get(account_id=user).employee_id
    orders = Orders.objects.filter(employee_id=employee_id_real)
    return render(request, 'myapp/employee_order_history.html', {'orders': orders})


def history_detail_employee(request, pk):
    order = Orders.objects.get(order_id=pk)
    order_details = OrderDetail.objects.filter(order_id=order)
    total_price = sum(detail.get_total_price() for detail in order_details) 
    return render(request, 'myapp/employee_history_order_detail.html', {
        'order': order,
        'order_details': order_details,
        'total_price': total_price
    })