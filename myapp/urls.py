from django.urls import path
from . import views
from .views import BookListView, BookDetailView, UserBookDetailView
urlpatterns =[
    path('',views.home , name='test-home'),
    path('order/', BookListView.as_view(), name='test-order'),
    path('order/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('employee/', views.employee, name='employee-home'),
    path('user/', views.user_home, name='user-home'),
    path('user/order/', views.user_order, name='user-order'),
    path('user/order/<int:pk>/', UserBookDetailView.as_view(), name='user-book-detail'),  
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),  
    path('user/cart/', views.Cart, name='cart'), 
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('user/order_history', views.order_history, name='user-order-history'),
    path('user/order_history/<int:pk>/', views.history_detail, name='history-detail'),
    path('employee/dashboard/', views.dashboard, name='employee-dashboard'),
    path('employee/inventory/', views.inventory, name='inventory-management'),
    path('employee/orders/', views.employee_orders, name='order-management'),
]