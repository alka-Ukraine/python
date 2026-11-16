from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name