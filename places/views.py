from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django.db.models import Q

from .models import Place
from .serializers import PlaceSerializer

class PlaceListView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        places = Place.objects.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(category__icontains=search)
        )
        return places