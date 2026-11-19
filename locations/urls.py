from django.urls import path
from .views import LocationListView, SearchHistoryListView

urlpatterns = [
    path('locations/', LocationListView.as_view()),
    path('search-history/', SearchHistoryListView.as_view()),
]