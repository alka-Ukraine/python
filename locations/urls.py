from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CityCoverViewSet, CityPostViewSet, InterestingPlaceViewSet, LocationDetailView, LocationListView, LoginView, RegisterView, SearchHistoryListView

router = DefaultRouter()
router.register('interesting-places', InterestingPlaceViewSet, basename='interesting-places')
router.register('city-covers', CityCoverViewSet, basename='city-covers')
router.register('city-posts', CityPostViewSet, basename='city-posts')

urlpatterns = [
    path('', include(router.urls)),
    path('locations/', LocationListView.as_view(), name='locations'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('search-history/', SearchHistoryListView.as_view(), name='search-history'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
