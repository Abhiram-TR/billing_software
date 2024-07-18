from django.db import models

class StockCurrent(models.Model):
    m_id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    material = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.material} - {self.quantity}"

class StockIn(models.Model):
    id=models.AutoField(primary_key=True)
    m_id = models.ForeignKey(StockCurrent, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.stock_current.material} - {self.quantity}"

class Bill(models.Model):
    invoice_number = models.CharField(max_length=50)
    material = models.CharField(max_length=255)
    date = models.DateField()
    bill_to_party = models.CharField(max_length=255)
    gstin_B = models.CharField(max_length=15)
    ship_to_party = models.CharField(max_length=255)
    gstin_s = models.CharField(max_length=15)
    hsn_code = models.CharField(max_length=20)
    rate_of_tax = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gross_value = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    stock_in = models.ForeignKey(StockIn, on_delete=models.CASCADE)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.material}"
