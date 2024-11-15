from django.contrib import admin
from .models import Book, Author, Publisher, Category \
, Customer, User, Orders, OrderDetail, Reviews
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Orders)
admin.site.register(OrderDetail)
admin.site.register(Reviews)
# Compare this snippet from myapp/models.py: