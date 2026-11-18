from rest_framework.generics import ListAPIView
from django.db.models import Q

from .models import Location, SearchHistory
from .serializers import LocationSerializer, SearchHistorySerializer


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')

        if search:
            SearchHistory.objects.create(query=search)

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.query_params.get('search', '')

        return Location.objects.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(category__icontains=search)
        )


class SearchHistoryListView(ListAPIView):
    queryset = SearchHistory.objects.order_by('-created_at')
    serializer_class = SearchHistorySerializer