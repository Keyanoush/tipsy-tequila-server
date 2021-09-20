from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .customer import Customer
from .product import Product

class Rating(models.Model):

    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
