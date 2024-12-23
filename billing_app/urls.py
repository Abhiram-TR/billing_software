from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('sell/', views.sell, name='sell'),
    path('print_bill/<int:pk>/', views.print_bill, name='print_bill'),
]
