from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from microblogs.forms import LogInForm, PostForm, SignUpForm
from microblogs.models import Post, User

# Create your views here.

def new_post(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            Post(author=request.user, text=text).save()
            messages.add_message(request, messages.SUCCESS, "Post created successfully")
            return redirect("feed")
        else:
            messages.add_message(request, messages.ERROR, "Invalid form data")
            render(request, "feed.html", {"form": PostForm()})
    else:
        messages.add_message(request, messages.ERROR, "You need to be logged in to make a post")
    return redirect("home")

def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    return render(request, "show_user.html", {"user": user})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})

def feed(request):
    form = PostForm()
    return render(request, 'feed.html', {"form": form})

def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.POST.get("next") or "feed"
                return redirect(redirect_url)
        
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    next = request.GET.get("next") or ""
    return render(request, 'log_in.html', {"form": form, "next": next})

def log_out(request):
    logout(request)
    return redirect("home")

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {"form": form})