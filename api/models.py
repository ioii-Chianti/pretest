from django.db import models


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)