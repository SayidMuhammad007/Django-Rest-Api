from django.db import models

# Create your models here.
class sell(models.Model):
    name = models.CharField(max_length=150)
    amount = models.CharField(max_length=100)
    price = models.CharField(max_length=150)
    date = models.DateField()
    time = models.CharField(max_length=50)
    status = models.IntegerField()
    price1 = models.CharField(max_length=120)
    user = models.IntegerField()
    product_id = models.IntegerField()

class product(models.Model):
    name = models.CharField(max_length=150)
    price1 = models.CharField(max_length=150)
    price2 = models.CharField(max_length=150)
    amount = models.CharField(max_length=100)
    date = models.DateField()

class sotilganlar(models.Model):
    name = models.CharField(max_length=150)
    price = models.CharField(max_length=150)
    customer = models.CharField(max_length=150)
    date = models.DateField()
    time = models.CharField(max_length=150)
    naqd = models.CharField(max_length=150)
    plastik = models.CharField(max_length=150)
    nasiya = models.CharField(max_length=150)
    amount = models.CharField(max_length=100)
    price1 = models.CharField(max_length=150)
    user = models.IntegerField()

class user(models.Model):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=50)
    position = models.CharField(max_length=50)