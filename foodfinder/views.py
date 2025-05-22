from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-publish_date")
    proc_questions = [
        dict(Question_id=q.id, Question=q.question_text) for q in latest_question_list
    ]

    output = {
        "total_questions": latest_question_list.count(),
        "questions_texts": proc_questions,
    }

    return JsonResponse(output)
