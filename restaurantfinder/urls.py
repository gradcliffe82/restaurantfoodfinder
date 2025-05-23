from django.urls import path
from .views import HomePage

urlpatterns = [
    path("restaurantfinder/", HomePage.as_view(), name="index"),
]