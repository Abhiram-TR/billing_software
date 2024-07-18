   
from django.urls import path
from .views import stock_in_create

urlpatterns = [
    path('', stock_in_create, name='stock_in_create'),
]
