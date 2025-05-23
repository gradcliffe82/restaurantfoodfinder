from django.db import models
from datetime import datetime as dt
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class Restaurants(models.Model):
    restaurant_ops = models.JSONField()

    weekday_dictionary = {
       0: "MON",
       1: "TUE",
       2: "WED",
       3: "THU",
       4: "FRI",
       5: "SAT",
       6: "SUN"
    }

    def find_open_restaurants(self, qry_timestamp):


        # get restaurants open today
        op_weekday = self.weekday_dictionary[qry_timestamp.weekday()]
        restaurants = Restaurants.objects.filter(restaurant_ops__days_open__contains=[op_weekday])
        if restaurants.count() == 0:
            return None

        # check restaurants operating time
        closed_restaurants = []
        for restaurant in restaurants:
            if not self._is_within_operating_hours(op_times=restaurant.restaurant_ops['operating_times'],
                                                   qry_time_dt = qry_timestamp):
                closed_restaurants.append(restaurant.id)

        open_restaurants = restaurants.exclude(id__in=closed_restaurants)
        if open_restaurants.count() == 0:
            return None

        return open_restaurants

    def _is_within_operating_hours(self, op_times, qry_time_dt):
        """
        Checks if current time is within operating hours
        """

        time_format = "%I:%M %p"
        opening_time = dt.strptime(op_times[0], time_format).time()
        closing_time = dt.strptime(op_times[1], time_format).time()
        qry_time_st = qry_time_dt.strftime("%I:%M:%S %p")
        current_time = dt.strptime(qry_time_st, "%I:%M:%S %p").time()
        return opening_time < current_time < closing_time
