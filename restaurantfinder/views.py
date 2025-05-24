from django.http import HttpResponseBadRequest, HttpRequest
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from restaurantfinder.models import Restaurants
from dateutil import parser
from datetime import datetime as dt
from zoneinfo import ZoneInfo
import re

from django.core.exceptions import ValidationError, PermissionDenied
# Create your views here.

@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomePage(TemplateView):
    template_name = "restaurantfinder/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RestaurantsView(View):
    error_message = {"error": ""}

    def get(self, request: HttpRequest, *args, **kwargs):
        approved_params = ["timestamp"]

        params = list(request.GET.keys())

        test_for_approved_params = [x for x in params if x not in approved_params]

        if len(test_for_approved_params) > 0:
            self.error_message['error'] = "Bad Request, invalid parameter found."
            return JsonResponse(self.error_message, status=400)

        try:
            timestamp = request.GET.dict()['timestamp']
        except Exception as ex:
            self.error_message['error'] = f"Bad Request, no valid parameter found: {ex}"
            return JsonResponse(self.error_message, status=400)

        # check formatting
        et_zone = ZoneInfo("America/New_York")
        if re.search(pattern=r"^\d{10}$", string=timestamp):
            # matches epoch timestamps, ex: 1747929600
            timestamp = dt.fromtimestamp(int(timestamp), tz=et_zone)
        elif re.search(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[\+\-]\d{2}:\d{2})$", string=timestamp):
            # matches 2025-05-23T10:23:00Z | 2025-05-23T10:23:00+05:30 | 2025-05-23T10:23:00-07:00
            parsed_dt = parser.isoparse(timestamp)
            timestamp = parsed_dt.astimezone(et_zone)

        elif re.search(pattern=r"^(\d{1,2})\/(\d{1,2})\/(\d{4}), (\d{1,2}):(\d{2}):(\d{2}) (AM|PM)$", string=timestamp):
            # matches the example: 5/23/2025, 11:00:00 AM
            dt_format = "%m/%d/%Y, %I:%M:%S %p"
            timestamp = dt.strptime(timestamp, dt_format)

        else:
            self.error_message['error'] = "Bad Request, invalid parameter value."
            return JsonResponse(self.error_message, status=400)

        # find open restaurants
        restaurants = Restaurants().find_open_restaurants(qry_timestamp=timestamp)
        if restaurants is None:
            output = {"restaurants": [], "total": 0}
            return JsonResponse(output)
        # return as json
        result_list = []
        for restaurant in restaurants:
            result_list.append(restaurant.restaurant_ops['restaurant_name'])

        data = {"open_restaurants": result_list, "total": len(result_list)}
        return JsonResponse(data)


def bad_request(request):
    return HttpResponseBadRequest(render(request, "400.html"))