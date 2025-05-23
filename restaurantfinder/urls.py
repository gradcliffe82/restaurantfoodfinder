from django.urls import path
from .views import HomePage, RestaurantsView, bad_request


urlpatterns = [
    path("restaurantfinder/", HomePage.as_view(), name="index"),
    path("restaurantfinder/search/", RestaurantsView.as_view(), name="search"),
]