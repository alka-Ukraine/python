from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LocationListView,
    SearchHistoryListView,
    InterestingPlaceViewSet,
)

router = DefaultRouter()
router.register(
    r'interesting-places',
    InterestingPlaceViewSet,
    basename='interesting-places'
)

urlpatterns = [
    path('', include(router.urls)),
    path('locations/', LocationListView.as_view()),
    path('search-history/', SearchHistoryListView.as_view()),
]