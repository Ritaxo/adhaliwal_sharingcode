from django.shortcuts import render

from django.http import HttpResponse

from share.models import Script

# Create your views here.
# Module 0
# def index(request):
#     if request.method == "GET":
#         return HttpResponse("Hello World!")

# Module 1
def get_first_script(request):
    if request.method == "GET":
        script = Script.objects.all()[0]
        return HttpResponse(str(script.title) + " " + str(script.description))


# Module 2
def index(request):
    if request.method == "GET":
        return render(request, 'share/index.html')  # new line
