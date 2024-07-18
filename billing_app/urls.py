from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('sell/', views.sell, name='sell'),
]
