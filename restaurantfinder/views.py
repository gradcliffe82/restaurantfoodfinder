from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpRequest, HttpResponseServerError
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import json
from django.core.exceptions import ValidationError, PermissionDenied
# Create your views here.

@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomePage(TemplateView):
    template_name = "restaurantfinder/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_posts'] = Post.objects.order_by("-post_date")

        return context