from django.db import models

# Create your models here.
class Warehouse(models.Model):
    COUNTRY = [
    ('Qatar', 'Qatar'),
    ('Oman', 'Oman'),
    ('Dubai','Dubai')
   
]
    country = models.CharField(max_length=20, choices=COUNTRY)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    streetnumber=models.CharField(max_length=200)
    warehousename=models.CharField(max_length=300)
    contact=models.CharField(max_length=20)

    def __str__(self):
        return self.country