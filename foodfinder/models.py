from django.db import models


class Restaurants(models.Model):
    restaurant_name = models.CharField(max_length=100)
    restaurant_operation = models.JSONField()
