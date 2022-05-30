from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User
from .forms import UserRegistrationForm,TodoForm,LogInForm
import requests,json
from .models import TodoItem

def register(request):
    ip= requests.get('https://api.ipify.org?format=json')
    ip_dic = json.loads(ip.text)
    #print(ip_dic)
    res = requests.get('http://ip-api.com/json/'+ip_dic["ip"])
    loc = res.text
    #print(loc)
    loc_data = json.loads(loc)

    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            user = User.objects.create(username=username,password=password1,latitude=loc_data['lat'],longitude=loc_data['lon'],country=loc_data['country'])
            user.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "todo/register.html", context)

@login_required
def home(request):
    user_data = User.objects.get(id=request.user.id)
    print(user_data)
    if request.method == 'POST':
        todo_name = request.POST.get("new-todo")
        todo = TodoItem.objects.create(name=todo_name, user=request.user)
        return redirect("home")

    todos = TodoItem.objects.filter(user=request.user, is_completed=False).order_by("-id")


    paginator = Paginator(todos, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"todos": todos, "page_obj": page_obj,"user_data":user_data}

    return render(request, "todo/crud.html", context,)

def logout_user(request):
    logout(request)
    return redirect("login")
    

def update_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.name = request.POST.get(f"todo_{pk}")
    todo.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def complete_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.is_completed = True
    todo.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def log_in(request):
    if request.method == "POST":
        print(request.POST)
        form = LogInForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.get(username=username, password=password)
            print(user)
            if user: 
                login(request, user)  
                return redirect('home')
            else: 
                error = True
    else:
        form = LogInForm()

    return render(request, 'todo/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('login')