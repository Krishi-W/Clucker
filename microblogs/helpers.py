from django.shortcuts import redirect
from django.conf import settings

def login_prohibited(view_function):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)

        return view_function(request)

    return wrapper