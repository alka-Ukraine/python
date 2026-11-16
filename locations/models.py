from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    description = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name