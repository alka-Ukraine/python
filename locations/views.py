
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from .models import Location, SearchHistory
from .serializers import (
    LocationSerializer,
    SearchHistorySerializer,
    RegisterSerializer,
)


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


class InterestingPlaceViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
