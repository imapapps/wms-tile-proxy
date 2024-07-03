# proxy/views.py
import json
from pathlib import Path

import requests
from django.http import HttpResponse
from urllib.parse import urljoin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from PIL import Image
import io

BASE_DIR = Path(__file__).resolve().parent.parent
f = open(str(BASE_DIR) + '/data.json', )
data = json.load(f)
THREDDS_SERVER_URL = data["THREDDS_SERVER_URL"]


def generate_transparent_image(width, height):
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return byte_arr


def proxy_wms_request(request, request_path):
    if request.user.is_authenticated and (request.user.is_staff or request.user.groups.filter(name='Private_Data_Viewer').exists()):
        # Construct the full URL to the internal THREDDS server
        internal_url = urljoin(THREDDS_SERVER_URL, request_path)

        # Get the query parameters from the original request
        query_params = request.META['QUERY_STRING']

        # Send the request to the internal server
        response = requests.get(f"{internal_url}?{query_params}")

        # Create a response to send back to the client
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    else:
        # Return a transparent image if the user is not authenticated
        width = int(request.GET.get('width', 256))
        height = int(request.GET.get('height', 256))
        transparent_image = generate_transparent_image(width, height)
        return HttpResponse(transparent_image, content_type="image/png")


def home(request):
    context = {
        "sample_layer_url": data["sample_layer_url"],
        "sample_layer_layers": data["sample_layer_layers"],
        "sample_layer_style": data["sample_layer_style"]
    }
    return render(request, "home.html", context)
