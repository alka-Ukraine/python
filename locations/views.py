import logging

from django.db import DatabaseError, connection
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CityCover, CityPost, Location, SearchHistory
from .serializers import CityCoverSerializer, CityPostSerializer, LocationSerializer, RegisterSerializer, SearchHistorySerializer


logger = logging.getLogger(__name__)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in ('GET', 'HEAD', 'OPTIONS') or (
            request.user.is_authenticated
            and getattr(obj, 'author_id', getattr(obj, 'uploaded_by_id', None)) == request.user.id
        )


class IsLocationAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in ('GET', 'HEAD', 'OPTIONS') or (
            request.user.is_authenticated
            and (request.user.is_staff or obj.submitted_by_id == request.user.id)
        )


class LocationListView(ListCreateAPIView):
    queryset = Location.objects.select_related('submitted_by').all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', '').strip()
        if search:
            user = request.user if request.user.is_authenticated else None
            try:
                SearchHistory.objects.create(query=search, user=user)
            except DatabaseError:
                logger.exception('Could not record search history')
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.query_params.get('search', '').strip()
        if search and connection.vendor == 'sqlite':
            term = search.casefold()
            matches = [
                pk for pk, name, city, country, category in Location.objects.values_list(
                    'pk', 'name', 'city', 'country', 'category'
                )
                if any(term in (value or '').casefold() for value in (name, city, country, category))
            ]
            return self.queryset.filter(pk__in=matches)
        return self.queryset.filter(
            Q(name__icontains=search)
            | Q(city__icontains=search)
            | Q(country__icontains=search)
            | Q(category__icontains=search)
        )

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class LocationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.select_related('submitted_by').all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsLocationAuthorOrReadOnly]


class SearchHistoryListView(ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user).order_by('-created_at')


class InterestingPlaceViewSet(ModelViewSet):
    queryset = Location.objects.select_related('submitted_by').all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsLocationAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class CityCoverViewSet(ModelViewSet):
    serializer_class = CityCoverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = CityCover.objects.select_related('uploaded_by').all()
        city = self.request.query_params.get('city', '').strip()
        return queryset.filter(city_key=city.casefold()) if city else queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class CityPostViewSet(ModelViewSet):
    serializer_class = CityPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = CityPost.objects.select_related('author').order_by('-created_at')
        city = self.request.query_params.get('city', '').strip()
        return queryset.filter(city_key=city.casefold()) if city else queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'register'


class LoginView(ObtainAuthToken):
    """Keep the existing token login available to older API clients."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})
