from django.contrib import admin
from .models import StockCurrent, StockIn, Bill

@admin.register(StockCurrent)
class StockCurrentAdmin(admin.ModelAdmin):
    list_display = ('m_id', 'material_name', 'quantity')
    search_fields = ('material_name',)
    list_filter = ('material_name',)

@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ('id', 'm_id', 'quantity', 'taxable_value', 'tax_percentage', 'date')
    search_fields = ('m_id__material_name', 'date')
    list_filter = ('date', 'tax_percentage')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'm_id', 'date', 'bill_to_party', 'ship_to_party', 'quantity', 'rate', 'amount', 'gross_value', 'total', 'sgst', 'cgst', 'grand_total')
    search_fields = ('invoice_number', 'm_id__material_name', 'bill_to_party', 'ship_to_party')
    list_filter = ('date', 'rate_of_tax')

# Registering the models without decorators:
# admin.site.register(StockCurrent, StockCurrentAdmin)
# admin.site.register(StockIn, StockInAdmin)
# admin.site.register(Bill, BillAdmin)
