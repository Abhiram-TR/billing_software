from django.shortcuts import render, redirect
from .forms import StockInForm

def stock_in_create(request):
    if request.method == 'POST':
        form = StockInForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'billing_app/index.html',{"message" : "successfull",'form': form})
    else:
        form = StockInForm()
    return render(request, 'billing_app/index.html', {'form': form})
