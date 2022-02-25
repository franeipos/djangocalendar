from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegisterUserForm, UserForm
# Create your views here.


def login_user(request):
    """
    Login user that has been signed up before.
    :param request:
    :return: returns list of calendars if the user is logged in or the login page otherwise.
    """

    if request.user.is_authenticated:
        return redirect('patients-list')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', None)
            if next_url is not None:
                return redirect(next_url)
            else:
                return redirect('patients-list')
        else:
            messages.error(request, 'ERROR: Nombre de usuario o contraseña incorrectas. Vuelva a intentarlo.')
            return redirect('login')
    else:
        next_url = request.GET.get('next', None)
        context = {'next': next_url}
        return render(request, 'authentication/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'EXITO: Se ha registrado correctamente.')
            return redirect('login')
    else:
        form = RegisterUserForm()

    context = {
        'form': form
    }
    return render(request, 'authentication/register_user.html', context)


def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }

    return render(request, 'user_data/user_detail.html', context)


def update_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        if user is not None:
            form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-detail', user.id)

    else:
        form = UserForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'user_data/update_user.html', context)
