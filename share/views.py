from django.shortcuts import render

# Create your views here.
# Module 0
from django.shortcuts import render
from django.http import HttpResponse
from share.models import Script

# Create your views here.
def index(request):
    if request.method == "GET":
        return HttpResponse("Hello World!")
