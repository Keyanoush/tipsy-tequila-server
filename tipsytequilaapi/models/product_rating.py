from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .rating import Rating


class ProductRating(models.Model):

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="products")
    rating = models.ForeignKey("Rating", on_delete=models.CASCADE, related_name="ratings")

