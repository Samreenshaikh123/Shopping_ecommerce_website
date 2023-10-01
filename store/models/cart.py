from django.db import models
from .product import Product

class Cart(models.Model):
    password = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
