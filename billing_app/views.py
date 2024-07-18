from django.http import HttpResponseBadRequest
from .models import StockCurrent, StockIn, Bill
from django.shortcuts import render, redirect
from .forms import StockInForm
from django.utils import timezone


def stock_in_create(request):
    if request.method == 'POST':
        form = StockInForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'billing_app/stock_in.html',{"message" : "successfull",'form': form})
    else:
        form = StockInForm()
    return render(request, 'billing_app/stock_in.html', {'form': form})


def dashboard(request):
    current_stock = StockCurrent.objects.all()
    recent_stock_ins = StockIn.objects.order_by('-date')[:10]  # last 10 stock ins
    recent_bills = Bill.objects.order_by('-date')[:10]  # last 10 bills

    context = {
        'current_stock': current_stock,
        'recent_stock_ins': recent_stock_ins,
        'recent_bills': recent_bills,
    }
    
    return render(request, 'billing_app/dashboard.html', context)



def add_stock(request):
    if request.method == 'POST':
        try:
            m_id = StockCurrent.objects.get(m_id=request.POST['m_id'])
            quantity = int(request.POST['quantity'])
            taxable_value = float(request.POST['taxable_value'])
            tax_percentage = float(request.POST['tax_percentage'])
            date = request.POST['date']

            stock_in = StockIn(
                m_id=m_id,
                quantity=quantity,
                taxable_value=taxable_value,
                tax_percentage=tax_percentage,
                date=date
            )
            stock_in.save()

            return redirect('dashboard')
        except StockCurrent.DoesNotExist:
            # Handle case where StockCurrent object with given id doesn't exist
            # You can redirect to an error page or handle the error appropriately
            return HttpResponseBadRequest('Invalid material id')
    materials = StockCurrent.objects.all()
    print(materials)
    return render(request, 'billing_app/add_stock.html', {'materials': materials})

def sell(request):
    if request.method == 'POST':
        invoice_number = request.POST['invoice_number']
        m_id = StockCurrent.objects.get(id=request.POST['m_id'])
        date = request.POST['date']
        bill_to_party = request.POST['bill_to_party']
        gstin_B = request.POST['gstin_B']
        ship_to_party = request.POST['ship_to_party']
        gstin_s = request.POST['gstin_s']
        hsn_code = request.POST['hsn_code']
        rate_of_tax = float(request.POST['rate_of_tax'])
        quantity = int(request.POST['quantity'])
        rate = float(request.POST['rate'])
        amount = float(request.POST['amount'])
        gross_value = float(request.POST['gross_value'])
        total = float(request.POST['total'])
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        grand_total = float(request.POST['grand_total'])
        stock_in = StockIn.objects.get(id=request.POST['stock_in'])

        bill = Bill(
            invoice_number=invoice_number,
            m_id=m_id,
            date=date,
            bill_to_party=bill_to_party,
            gstin_B=gstin_B,
            ship_to_party=ship_to_party,
            gstin_s=gstin_s,
            hsn_code=hsn_code,
            rate_of_tax=rate_of_tax,
            quantity=quantity,
            rate=rate,
            amount=amount,
            gross_value=gross_value,
            total=total,
            sgst=sgst,
            cgst=cgst,
            grand_total=grand_total,
        )
        bill.save()

        return redirect('dashboard')

    materials = StockCurrent.objects.all()
    return render(request, 'billing_app/sell.html', {'materials': materials})