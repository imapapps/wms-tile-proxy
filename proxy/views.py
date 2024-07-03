# proxy/views.py
import json
from pathlib import Path

import requests
from django.http import HttpResponse
from urllib.parse import urljoin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent
f = open(str(BASE_DIR) + '/data.json', )
data = json.load(f)
THREDDS_SERVER_URL = data["THREDDS_SERVER_URL"]


@login_required
def proxy_wms_request(request, request_path):
    # You will have to add some logic here to confirm the logged-in user has access to the wms he is requesting.
    # This can be done with groups or query to db if you have a relationship between users and the wms data assets

    # Construct the full URL to the internal THREDDS server
    internal_url = urljoin(THREDDS_SERVER_URL, request_path)

    # Get the query parameters from the original request
    query_params = request.META['QUERY_STRING']

    # Send the request to the internal server
    response = requests.get(f"{internal_url}?{query_params}")

    # Create a response to send back to the client
    return HttpResponse(response.content, content_type=response.headers['Content-Type'])


def home(request):
    return render(request, "home.html", context={})
