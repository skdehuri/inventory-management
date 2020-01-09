from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse


def home(request):
    """
    Function to get home page
    :param request: request received from web server
    :return: renders home
    """
    context = {}
    try:
        is_store_manager = request.user.groups.filter(name='Store Manager').exists()
        context.update({'is_store_manager': is_store_manager})
    except Exception as e:
        pass
    return render(request, 'home.html', context)


def login(request):
    """
    Function used to login the user
    :param request: request received from web server
    :return: renders home if user exists
    """
    try:
        if request.method == 'POST':
            request_data = request.POST
            username = request_data.get('username')
            password = request_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                user_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Invalid login details given")
        else:
            return render(request, 'login.html', {})
    except Exception as e:
        return HttpResponse("something went wrong")


@login_required
def logout(request):
    """
    Function used to logout the user
    :param request: request received from web server
    :return: logs out the user
    """
    try:
        user_logout(request)
        return HttpResponseRedirect(reverse('home'))
    except Exception as e:
        return HttpResponse("something went wrong")
