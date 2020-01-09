from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse


def login(request):
    """
    Function used to login the user
    :param request: request received from web server
    :return: renders home if user exists
    """
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                request_data = request.POST
                username = request_data.get('username')
                password = request_data.get('password')
                user = authenticate(username=username, password=password)
                if user:
                    user_login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse('Invalid Username/Password')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    except Exception as e:
        return HttpResponse("Something went wrong")


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
