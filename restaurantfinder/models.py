from django.db import models


class Restaurants(models.Model):
    restaurant_ops = models.JSONField()
