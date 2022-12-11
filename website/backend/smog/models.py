from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class SmogPrediction(models.Model):
    date = models.DateField(null=False)
    prediction = models.IntegerField(validators=[
            MaxValueValidator(2),
            MinValueValidator(0)
        ])