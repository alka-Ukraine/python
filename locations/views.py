from rest_framework.generics import ListAPIView
from django.db.models import Q

from .models import Location
from .serializers import LocationSerializer


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', '')

        return Location.objects.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(category__icontains=search)
        )