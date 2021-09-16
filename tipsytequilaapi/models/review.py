from django.db import models


class Review(models.Model):

    description = models.CharField(max_length=255)

    