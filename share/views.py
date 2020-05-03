from django.shortcuts import render

from django.http import HttpResponse

from share.models import Script

from django.shortcuts import render, get_object_or_404

# Module 3 imports
# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout

# import redirect
from django.shortcuts import render, redirect

# import all the models created so far
#from .models import Script, Problem, Coder

# import User model
from django.contrib.auth.models import User

from .models import Script, Problem, Coder, Review

# at the top
from share.find_offensive_language import offensive


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

def build_script(request, problem_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            problem = get_object_or_404(Problem, pk = problem_id )
            return render(request, "share/build_script_form.html", {"user": user, "problem":problem})


def create_script(request, problem_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        problem = get_object_or_404(Problem, pk = problem_id)

        if not request.POST["title"]: #this does not work with textares form elements
            return render(request, "share/build_script_form.html", {"user": user, "problem":problem, "error":"One of the required fields was empty"})

        else:
            coder = user.coder
            title = request.POST["title"]
            description = request.POST["description"]
            code = request.POST["code"]
            url = request.POST["url"]
            input = request.POST["input"]
            output = request.POST["output"]
            working_code = request.POST.get('working_code', False)
            make_public = request.POST.get('make_public', False)

            if working_code == 'on':
                working_code = True
            else:
                working_code = False

            if make_public == 'on':
                make_public = True
            else:
                make_public = False

        # Validate URL in Script (for future work)
            """
           try:
               URLValidator()(url)
           except:
               return render(request, "share/build_script_form.html", {"error":"URL is not valid"})
           """

            try:
                script = Script.objects.create(coder=coder, problem=problem, title=title, description=description, code=code, url=url, input=input, output=output, working_code=working_code, make_public=make_public)
                script.save()

                script = get_object_or_404(Script, pk=script.id)
                problem = get_object_or_404(Problem, pk=problem_id)
                return render(request, "share/script.html",{"user":user, "problem":problem, "script": script})

            except:
                return render(request, "share/build_script_form.html", {"error":"Can't create the script"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't create!"})
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


def publish_problem(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            return render(request, "share/publish_problem_form.html", {"user":user} )

def create_problem(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        coder = user.coder
        title = request.POST["title"]
        description = request.POST["description"]
        discipline = request.POST["discipline"]
        make_public = request.POST.get('make_public', False)
        if make_public == 'on':
            make_public = True
        else:
            make_public = False

        if not title and not description:
            return render(request, "share/publish_problem_form.html", {"error":"Please fill in all required fields"})

        try:
            problem = Problem.objects.create(coder=coder, title=title, description=description, discipline=discipline, make_public=make_public)
            problem.save()

            problem = get_object_or_404(Problem, pk=problem.id)
            scripts = Script.objects.filter(problem=problem.id)

            return render(request, "share/problem.html",{"user":user, "problem":problem, "scripts": scripts})

        except:
            return render(request, "share/publish_problem_form.html", {"error":"Can't create the problem"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't create!"})
# Module 4
def show_problem(request, problem_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            problem = get_object_or_404(Problem, pk=problem_id)
            scripts = Script.objects.filter(problem=problem_id)
            user_script = Script.objects.filter(coder=user.id).filter(problem=problem.id)

            # Module 6
            if problem.make_public or problem.coder.user.id == user.id:
                return render(request, "share/problem.html",
                {"user":user, "problem":problem, "scripts": scripts})
            else:
                # the problem is private and you are not the author
                return render(request, "share/index.html",
                {"error":"The problem you clicked is still private and you are not the author"})

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

def show_script(request, script_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            script = get_object_or_404(Script, pk=script_id)
            problem = get_object_or_404(Problem, pk=script.problem.id)

            # Module 10
            reviews = Review.objects.filter(script=script_id)
            print("******************************")
            print(reviews)

            # Module 7
            if script.coder.user.id == user.id or script.make_public:
                return render(request, "share/script.html",
                {"user":user, "problem":problem, "script": script})
            else:
                # you are not the author
                 # you are not the author
                all_problems = Problem.objects.all()
                return render(request, "share/index.html",
                {"user":user, "all_problems": all_problems,
                "error":"The script you clicked is not public and you are not the author"})

def edit_problem(request, problem_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        problem = get_object_or_404(Problem, pk=problem_id)

        # does this problem have any scripts? if yes you can't update or delete
        scripts = Script.objects.filter(problem=problem_id)

        if problem.coder.user.id == user.id:
            return render(request, "share/edit_problem.html", {"problem":problem})
        else:
            return render(request, "share/index.html",
            {"error":"You are not the author of the problem that you tried to edit."})

        if problem.coder.user.id == user.id and not scripts and not problem.make_public:
            return render(request, "share/edit_problem.html", {"problem":problem})
        else:
            return render(request, "share/index.html",
            {"error":"You are not the author of the problem that you tried to edit."})


def update_problem(request, problem_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        problem = get_object_or_404(Problem, pk=problem_id)
        scripts = Script.objects.filter(problem=problem_id)

        if not request.POST["title"] or not request.POST["description"] or not request.POST["discipline"]:
            return render(request, "share/edit_problem.html", {"problem":problem,
            "error":"One of the required fields was empty"})

        else:
            title = request.POST["title"]
            description = request.POST["description"]
            discipline = request.POST["discipline"]

            make_public = request.POST.get('make_public', False)

            print('***********************')
            print('user input make_public:', make_public)    # it shows as on

            if make_public == 'on':
                make_public = True
            else:
                make_public = False

            print('******** Testing *************')
            print('make_public:', make_public)
            print('***********************')

            if problem.coder.user.id == user.id and not scripts and not problem.make_public:
                Problem.objects.filter(pk=problem_id).update(title=title, description=description, discipline=discipline, make_public=make_public)
                return redirect("share:dashboard")

            else:
                return render(request, "share/edit_problem.html",{"problem":problem, "error":"Can't update!"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/update
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't update!"})

def update_script(request, script_id):
    if request == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        script = get_object_or_404(Script, pk = script_id)
        problem = get_object_or_404(Problem, pk = script.problem.id)

        if not request.POST["title"]: #this does not work with testarea form elements
            return render(request, "share/edit_script.html", {"user":user, "script":script, "error":"One of the required fields was empty"})

        else:
            title = request.POST["title"]
            description = request.POST["description"]
            code = request.POST["code"]
            url = request.POST["url"]
            input = request.POST["input"]
            output = request.POST["output"]
            working_code = request.POST.get("working_code", False)
            make_public = request.POST.get("make_public", False)

            if working_code == "on":
                working_code = True

            else:
                working_code = False

            if make_public == "on":
                make_public = True
            else:
                make_public = False

            if script.coder.user.id == user.id:
                Script.objects.filter(pk = script.id).update(title= title, description=description, code=code, url= url, output=output, input=input, make_public=make_public, working_code= working_code)

                script = get_object_or_404(Script, pk = script_id) #get new updated record

                return render(request, "share/script.html", {"user":user, "problem":problem, "script":script, "error":"Script Updated!"})

            else:
                #the user entering the http://127.0.0.1:18000/problem/8/update

                user = request.user
                all_problems = Probelm.objects.all()
                return render(request, "share/index.html",{"user":user, "script":script, "problem":probelm, "error":"IT was not a POST request!"})


def delete_problem(request, problem_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        problem = get_object_or_404(Problem, pk=problem_id)
        scripts = Script.objects.filter(problem=problem_id)

        if problem.coder.user.id == user.id and not scripts and not problem.make_public:
            Problem.objects.get(pk=problem_id).delete()
            return redirect("share:dashboard")
        else:
            all_problems = Problem.objects.all()
            return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't delete!"})

    else:
        return HttpResponse(status=500)

# if script doesnt exist error should load

def delete_script(request, script_id):
    if request.method =="POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status = 500)

        script = get_object_or_404(Script, pk = script_id)
        if script.coder.user.id  == user.id:
            Script.objects.get(pk = script_id).delete()
            return redirect("share:dashboard")
        else:
            all_problems = Problem.objects.all()
            return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't delete the script!"})
    else:
        return HttpResponse(status=500)


def edit_script(request, script_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        script = get_object_or_404(Script, pk = script_id)
        problem = get_object_or_404(Problem, pk = script.problem.id)

        if script.coder.user.id == user.id:
            return render(request, "share/edit_script.html", {"user":user, "script":script})
        else:
            return render(request, "share/edit_script.html", {"user":user, "script":script, "problem":problem, "error":"You can't edit this script!"})

def create_review(request,script_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        script = get_object_or_404(Script, pk=script_id)
        problem = get_object_or_404(Problem, pk=script.problem.id)

        coder = user.coder
        feedback = request.POST["feedback"]

        stars = request.POST.get('stars', False)
        print('************************')
        print(stars)

        if stars == 'Confusing':
            stars = 1
        elif stars ==  "Clear":
            stars = 2
        else:
            stars = 3

        try:
            if offensive(feedback):
                 reviews = Review.objects.filter(script=script_id)
                 user_review = Review.objects.filter(coder=user.id).filter(script=script.id)

                 return render(request, "share/script.html",
               {"user":user, "problem":problem, "script": script, "reviews":reviews, "user_review":user_review, "error":"Can't create the review with offensive language"})

            review = Review.objects.create(coder=coder, script=script, feedback=feedback, stars=stars)
            review.save()
            # script.html  needs user, script, problem, reviews, user_review
            reviews = Review.objects.filter(script=script_id)
            user_review = Review.objects.filter(coder=user.id).filter(script=script.id)

            return render(request, "share/script.html",
            {"user":user, "problem":problem, "script": script, "reviews":reviews, "user_review":user_review})

        except:
            return render(request, "share/script.html", {"error":"Can't create the script"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't create review!"})

def delete_review(request, review_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        review = get_object_or_404(Review, pk=review_id)

        # script.html needs user, script, problem, reviews, user_review
        script = get_object_or_404(Script, pk=review.script.id)
        problem = get_object_or_404(Problem, pk=script.problem.id)


        if review.coder.user.id == user.id:
            Review.objects.get(pk=review_id).delete()

            reviews = Review.objects.filter(script=script.id)
            user_review = Review.objects.filter(coder=user.id).filter(script=script.id)  # should retrive no obj

            return render(request, "share/script.html",
            {"user":user, "problem": problem, "script":script, "reviews":reviews, "user_review":user_review,
            "error":"Review deleted!"})

        else:
            user_review = Review.objects.filter(coder=user.id).filter(script=script.id)  # should retrive no obj

            return render(request, "share/script.html",
            {"user":user, "problem": problem, "script":script, "reviews":reviews, "user_review":user_review, "error":"Can't delete the review!"})

    else:
        return HttpResponse(status=500)

# Module 11
def search(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        query = request.POST["query"]

        if not query:
            return render(request, "share/search_result.html", {"error":"Empty search"})

        scripts = Script.objects.filter(title__icontains=query) | Script.objects.filter(description__icontains=query)

        return render(request, "share/search_result.html", {"user":user, "scripts":scripts, "query":query})
    else:
        return HttpResponse(status=500)
