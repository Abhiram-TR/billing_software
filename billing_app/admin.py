
# Register your models here.
# your_app/admin.py

from django.contrib import admin
from .models import StockIn, Bill,StockCurrent

# Register your models here.

admin.site.register(StockIn)
admin.site.register(Bill)
admin.site.register(StockCurrent)