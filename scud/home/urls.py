from django.urls import path
from .views import Home, Base, Detail, SearchResultsView


urlpatterns = [
    path('', Home, name='home'),
    path('base/<int:pk>', Base, name='base'),
    path('base/<int:pk>/detail', Detail, name='detail'),
    path('search', SearchResultsView.as_view(), name='search'),
]
