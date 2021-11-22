from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

from microblogs.forms import PasswordForm, UserForm, LogInForm, PostForm, SignUpForm
from microblogs.models import Post, User

from microblogs.helpers import login_prohibited

# Create your views here.

@login_required
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('feed')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('feed')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})


def new_post(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            Post(author=request.user, text=text).save()
            messages.add_message(request, messages.SUCCESS, "Post created successfully")
        else:
            messages.add_message(request, messages.ERROR, "Invalid form data")
        return redirect("feed")
    else:
        messages.add_message(request, messages.ERROR, "You need to be logged in to make a post")
    return redirect("home")

@login_required
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
    except User.DoesNotExist:
        return redirect("user_list")
    else:
        return render(request, "show_user.html", {"user": user, "posts": posts})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})

@login_required
def feed(request):
    form = PostForm()
    posts = Post.objects.filter(author=request.user)
    return render(request, 'feed.html', {"form": form, "posts": posts})

@login_prohibited
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

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_prohibited
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