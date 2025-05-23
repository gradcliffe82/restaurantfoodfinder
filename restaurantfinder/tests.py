from django.test import TestCase
from django.db import models
from .models import Restaurants

class RestaurantsTestCase(TestCase):

    def _create_records(self):
        self.restaurant = Restaurants.objects.create(
            restaurant_ops = {
                'days_open': ['MON', 'TUE', 'TUES', 'WED','THU', 'FRI', 'SAT'],
                'operating_times': ['11:00 AM', '10:00 PM'],
                'restaurant_name': 'The Cowfish Sushi Burger Bar'}
        )

        self.restaurant = Restaurants.objects.create(
            restaurant_ops={
                'days_open': ['MON', 'TUE', 'TUES', 'WED', 'THU', 'FRI', 'SAT'],
                'operating_times': ['11:00 AM', '11:00 PM'],
                'restaurant_name': 'The Cowfish Sushi Burger Bar'}
        )
    def setUp(self):
        self._create_records()

    def test_restaurant_open(self):
        # 5/22/2025 11:00 AM - THU
        qry_timestamp = "1747926000"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 2)


        # 5/21/2025 6:00 PM - WED
        qry_timestamp = "1747850400"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 2)

        # # 5/19/2025 6:00 PM - MON
        # qry_timestamp = "1747702800"
        # restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        # self.assertEqual(restaurants.count(), 2)

    def test_restaurant_nothing_open(self):
        # 5/22/2025 11:00 PM - THU
        qry_timestamp = "1747969200"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 0)

        # 5/25/2025 11:00 PM - SUN
        qry_timestamp = "1748228400"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 0)