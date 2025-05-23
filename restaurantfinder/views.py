from django.http import HttpResponseNotFound, HttpRequest, HttpResponseServerError
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import BadRequest
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
        # context['latest_posts'] = Post.objects.order_by("-post_date")

        return context


class RestaurantsView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        approved_params = ["timestamp"]
#1747929600 "2025-05-23T10:23:00Z"
    #
        params = list(request.GET.keys())

        test_for_approved_params = [x for x in params if x not in approved_params]
        if len(test_for_approved_params)>0:
            raise BadRequest("Bad Request. Invalid parameters found.")

        try:
            timestamp = request.GET.dict()['timestamp']
        except Exception as ex:
            raise BadRequest("Bad Request. Parameter not found")
        # check formatting
        et_zone = ZoneInfo("America/New_York")
        if re.search(pattern=r"^\d{10}$", string=timestamp):
            # matches epoch timestamps, ex: 1747929600
            timestamp = dt.fromtimestamp(int(timestamp), tz=et_zone)
        elif re.search(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[\+\-]\d{2}:\d{2})$", string=timestamp):
            parsed_dt = parser.isoparse(timestamp)
            timestamp = parsed_dt.astimezone(et_zone)

        elif re.search(pattern=r"^(\d{1,2})\/(\d{1,2})\/(\d{4}), (\d{1,2}):(\d{2}):(\d{2}) (AM|PM)$", string=timestamp):
            # matches the example: 5/23/2025, 11:00:00 AM
            dt_format = "%m/%d/%Y, %I:%M:%S %p"
            timestamp = dt.strptime(timestamp, dt_format)

        else:
            raise BadRequest("Bad Request. Invalid Timestamp")
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
