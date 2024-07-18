
from django.db import models
from django.db.models import Max
class StockCurrent(models.Model):
    m_id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    material_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.material_name} - {self.quantity}"

class StockIn(models.Model):
    m_id = models.ForeignKey(StockCurrent, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date = models.DateField()
    
    def save(self, *args, **kwargs):
        # Add the quantity to the stock_current table
        self.amount = self.taxable_value + (self.taxable_value * (self.tax_percentage / 100))
        super().save(*args, **kwargs)
        if self.quantity > 0:
            self.m_id.quantity += self.quantity
            self.m_id.save()

    def __str__(self):
        return f"{self.m_id.material_name} - {self.quantity}"

class Bill(models.Model):
    invoice_number = models.CharField(max_length=20, editable=False, unique=True)
    m_id = models.ForeignKey(StockCurrent, on_delete=models.CASCADE)
    date = models.DateField()
    bill_to_party = models.CharField(max_length=255)
    gstin_B = models.CharField(max_length=15)
    ship_to_party = models.CharField(max_length=255)
    gstin_s = models.CharField(max_length=15)
    hsn_code = models.CharField(max_length=20)
    rate_of_tax = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    gross_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            max_invoice_number = Bill.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
            if max_invoice_number:
                self.invoice_number = str(int(max_invoice_number) + 1).zfill(6)  # Padded to 6 digits
            else:
                self.invoice_number = '000001'
        # Calculate amount as rate * quantity
        self.amount = self.rate * self.quantity
        self.gross_value = self.amount
        self.total = self.amount

        # Calculate grand_total
        self.grand_total = self.total + (self.total * (self.rate_of_tax / 100))
        
        
        # Remove quantity from stock
        if self.quantity <= self.m_id.quantity:
            self.m_id.quantity -= self.quantity
            self.m_id.save()
        else:
            raise ValueError("Insufficient stock quantity")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.m_id.material_name}"
