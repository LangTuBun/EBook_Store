from django.urls import path
from . import views
from .views import BookListView, BookDetailView
urlpatterns =[
    path('',views.home , name='test-home'),
    path('order/', BookListView.as_view(), name='test-order'),
    path('order/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('employee/', views.employee, name='employee-home'),
    path('user/', views.user_home, name='user-home'),
]