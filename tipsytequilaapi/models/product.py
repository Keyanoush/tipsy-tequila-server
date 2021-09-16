from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .customer import Customer


class Product(SafeDeleteModel):

    name = models.CharField(max_length=50,)
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name='products')
    price = models.FloatField(
        validators=[MinValueValidator(0.00), MaxValueValidator(10000.00)],)
    description = models.CharField(max_length=255,)
    quantity = models.IntegerField(validators=[MinValueValidator(0)],)
    created_date = models.DateField(auto_now_add=True)
    image_path = models.ImageField(
        upload_to='products', height_field=None,
        width_field=None, max_length=None, null=True)

    