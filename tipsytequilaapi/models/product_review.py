from django.db import models
from .review import Review
from .product import Product


class ProductReview(models.Model):

    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product")
    review = models.ForeignKey("Review", on_delete=models.CASCADE, related_name="review")
