from django.conf import settings
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    description = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='submitted_locations',
    )

    def __str__(self):
        return self.name

class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='search_history',
    )

    def __str__(self):
        return self.query


class CityCover(models.Model):
    city = models.CharField(max_length=100, unique=True)
    city_key = models.CharField(max_length=100, unique=True, editable=False)
    image = models.ImageField(upload_to='city-covers/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city

    def save(self, *args, **kwargs):
        self.city = self.city.strip()
        self.city_key = self.city.casefold()
        super().save(*args, **kwargs)


class CityPost(models.Model):
    city = models.CharField(max_length=100, db_index=True)
    city_key = models.CharField(max_length=100, db_index=True, editable=False)
    title = models.CharField(max_length=160)
    body = models.TextField()
    image = models.ImageField(upload_to='city-posts/', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.city = self.city.strip()
        self.city_key = self.city.casefold()
        super().save(*args, **kwargs)
