import os
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Bill

def generate_bill_pdf(bill):
    template_path = 'billing_app/bill_template.html'
    context = {
        'bill': bill,
        'sgst': bill.total * bill.rate_of_tax / 200,
        'cgst': bill.total * bill.rate_of_tax / 200,
    }
    
    template = get_template(template_path)
    html = template.render(context)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        pdf_path = os.path.join('bill_pdfs', f'bill_{bill.invoice_number}.pdf')
        with open(pdf_path, 'wb') as output:
            output.write(result.getvalue())
        return pdf_path
    else:
        return None


def render_pdf_view(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    pdf_path = generate_bill_pdf(bill)
    
    if pdf_path:
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename=bill_{bill.invoice_number}.pdf'
            return response
    else:
        return HttpResponse("Error generating PDF", status=400)
