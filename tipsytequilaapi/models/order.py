from django.db import models
from .customer import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
    purchased = models.BooleanField(default=False)
    created_date = models.DateField(default="0000-00-00",)