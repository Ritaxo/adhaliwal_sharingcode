from django.shortcuts import render

from django.http import HttpResponse

from share.models import Script

# Module 3 imports
# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout

# import redirect
from django.shortcuts import render, redirect

# import all the models created so far
from .models import Script, Problem, Coder

# import User model
from django.contrib.auth.models import User

# Module 1
def get_first_script(request):
    if request.method == "GET":
        script = Script.objects.all()[0]
        return HttpResponse(str(script.title) + " " + str(script.description))


# Module 2
def index(request):
    # if request.method == "GET":
    #     return render(request, 'share/index.html')  # new line
    # Testing http request object inside a view function
    print('*********** Testing request obj ************')
    print('request:' , request)
    print('request.headers: ', request.headers)
    print('request.headers["host"]:', request.headers['host'])
    print('request.method: ', request.method)
    print('request.user:' , request.user)
    print('*******************************')

    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            all_problems = Problem.objects.all()   # all_problems is a list object [   ]

            return render(request, "share/index.html", {"user":user, "all_problems": all_problems})
        else:
            return redirect("share:login")
    else:
        return HttpResponse(status=500)
# Module 3 Authentication functions

def signup(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/signup.html')

def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        coder_yet = request.POST['coder_yet_checkbox']

        if username is not None and email is not None and password is not None: # checking that they are not None
            if not username or not email or not password: # checking that they are not empty
                return render(request, "share/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "share/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "share/signup.html", {"error": "Email already exists"})
        # save our new user in the User model
        user = User.objects.create_user(username, email, password)
        coder = Coder.objects.create(user= user, coder_yet = coder_yet).save()
        user.save()

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        # this logs in our new user, backend means that we are using the  Django specific auhentication and not 3rd party

        return redirect("share:index")

    else:
        return redirect("share:signup")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/login.html')

# the function loguser is called from the login form
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            return render(request, "share/login.html", {"error":"One of the fields was empty"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("share:index")
        else:
            return render(request, "share/login.html", {"error":"Wrong username or password"})
    else:
        return redirect("share:index")

def logout_view(request):
    logout(request)
    return redirect("share:login")

def dashboard_view(request):
    pass
def publish_problem(request):
    pass

# Module 4
def show_problem(request, problem_id):
    pass
def show_my_problem(request, problem_id):
    pass

def show_my_script(request, problem_id):
    pass
# Module 4 testing
def dashboard(request):
    # retieve user, my_problems, my-scripts
    # builds my_problems_scripts dict
    # renders dashboard.html
    # each problem should have a link show more details of a particular problem,
    # this link starts route show_my_problem

    # Testing http request object inside a view function
    print('*********** Testing request obj ************')
    print('request:' , request)
    print('request.headers: ', request.headers)
    print('request.headers["host"]:', request.headers['host'])
    print('request.method: ', request.method)
    print('request.user:' , request.user)
    print('*******************************')

    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            my_problems = Problem.objects.filter(coder=user.coder.id)   # Problem table has a coder field (FK)
            my_scripts =  Script.objects.filter(coder=user.coder.id)

            print('*********** Testing objs retrieved from DB ************')
            print('my_problems:', my_problems)
            print('my_scripts:', my_scripts)
            print('*******************************')

            return render(request, "share/dashboard.html", {"my_scripts": my_scripts, "my_problems": my_problems })
