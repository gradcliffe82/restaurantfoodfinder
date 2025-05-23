from django.test import TestCase
from django.db import models
from .models import Restaurants

class RestaurantsTestCase(TestCase):

    def _create_records(self):
        self.restaurant = Restaurants.objects.create(
            restaurant_ops = {
                'days_open': ['MON', 'TUE', 'WED','THU', 'FRI', 'SAT'],
                'operating_times': ['11:00 AM', '10:00 PM'],
                'restaurant_name': 'The Cowfish Sushi Burger Bar'}
        )

        self.restaurant = Restaurants.objects.create(
            restaurant_ops={
                'days_open': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'],
                'operating_times': ['11:00 AM', '11:00 PM'],
                'restaurant_name': 'The Cowfish Sushi Burger Bar'}
        )
    def setUp(self):
        self._create_records()

    def test_restaurant_open(self):
        # all timestamps are in GMT

        # 5/22/2025 12:00 PM - THU
        qry_timestamp = "1747929600" # "1747926000"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 2)

        # 5/19/2025 11:01 AM - MON
        qry_timestamp = "1747666860"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 2)

        # 5/24/2025 09:30 PM - SAT
        qry_timestamp = "1748136600"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 2)

        # 5/24/2025 10:00 PM - MON
        qry_timestamp = "1748138400"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 1)

    def test_restaurant_nothing_open(self):
        # 5/22/2025 11:00 PM - THU - outside working hours
        qry_timestamp = "1747969200"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 0)

        # 5/25/2025 11:00 PM - SUN - closed sunday
        qry_timestamp = "1748228400"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertIsNone(restaurants)

        # 5/23/2025 8:30 AM - THU - outside working hours
        qry_timestamp = "1748003400"
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=qry_timestamp)
        self.assertEqual(restaurants.count(), 0)

