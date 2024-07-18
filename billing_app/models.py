from django.db import models

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
    date = models.DateField()
    
    def save(self, *args, **kwargs):
        #add the quantity to the stock_current table
        super().save(*args, **kwargs)
        if self.quantity > 0:
            self.m_id.quantity += self.quantity
            self.m_id.save()

    
    def __str__(self):
        return f"{self.m_id.material_name} - {self.quantity}"

class Bill(models.Model):
    invoice_number = models.CharField(max_length=50)
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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gross_value = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        #remove quantity from stock
        if self.quantity >= self.m_id.quantity:
            self.m_id.quantity -= self.quantity
            self.m_id.save()
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.m_id.material_name}"
