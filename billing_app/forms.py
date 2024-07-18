from django import forms
from .models import StockIn

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ['m_id', 'quantity', 'taxable_value', 'tax_percentage', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
