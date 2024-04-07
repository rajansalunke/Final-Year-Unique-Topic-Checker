from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.verify import authentication
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from datetime import datetime
from .process import *
from .models import Results
# Create your views here.
def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    # return HttpResponse("This is Home page")    
    return render(request, "log_in.html")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
    # return HttpResponse("This is Home page")    
    return render(request, "register.html")


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'fname' : request.user.first_name,
    }
    if request.method == "POST":
        user_title = request.POST['user_title']
        user_abstract = request.POST['user_abstract']
        user_algorithm = request.POST['user_algorithm']
        user_methodology = request.POST['user_methodology']
        
        result = find_matches(user_title, user_abstract, user_algorithm, user_methodology)
        save_data = Results.objects.create(title = user_title, abstract = user_abstract, algorithm = user_algorithm, methodology = user_methodology, results = result)
        save_data.save()
        messages.success(request, "Result Generated !!")
        return redirect("result")
    return render(request, "dashboard.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def result(request):
    result_data = Results.objects.last()
    matches = eval(result_data.results)
    context = {
        'fname': request.user.first_name,
        'results': result_data,
        'matched_data': matches,
    }
    
    return render(request, "result.html", context)