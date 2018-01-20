# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from .imcomposer import imcomposer
import logging
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

logger = logging.getLogger(__name__)


# Create your views here.

@csrf_exempt
def create_movie(request):
    data = request.POST
    if 'email' not in data:
        return JsonResponse({'message': "'email' is required."}, status=400)
    logger.info("Creating Movie for request: {0}".format(data))
    res = imcomposer.start_compose(data)
    return JsonResponse(dict(zip(("request_id", "job_id"), res)))


@csrf_exempt
def job_status(request):
    data = json.loads(request.body.decode("utf-8"))
    job_id = data['job_id']
    logger.info("Finding Status for Job: {0}".format(data['job_id']))
    status = imcomposer.job_status(job_id)
    logger.info("Job Status is : {0}".format(status))
    return JsonResponse({"job_status": status})

def get_insurance(request):
    return render(request, 'insurance_generation.html')


def get_success(request):
    request_id = request.GET.get("request_id")
    job_id = request.GET.get("job_id")
    #TODO: Write a logic to get URL
    url = ""
    return render(request, 'success.html', {"url": url})

