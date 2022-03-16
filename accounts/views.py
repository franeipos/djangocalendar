from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from .forms import RegisterUserForm, UserForm, TherapistForm
# Create your views here.
from .token import account_activation_token


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
            try:
                # Verify if the user exists but its account is not active.
                user_temp = User.objects.filter(username=username)
            except:
                messages.error(request,
                               'ERROR: Nombre de usuario o contraseña incorrectas. Vuelva a intentarlo.')
            else:
                messages.error(request,
                               'ERROR: Su cuenta no ha sido activdada. Por favor, revise su correo y actívela.')

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
        form_user = RegisterUserForm(request.POST)
        form_therapist = TherapistForm(request.POST)

        if form_user.is_valid() and form_therapist.is_valid():
            # Save user info and verify is is not active until email conrfirmation.
            user = form_user.save()
            user.is_active = True
            user.save()

            # Save the therapist extra info associated to the user.
            print(form_therapist.cleaned_data)
            user.therapist.institution = form_therapist.cleaned_data.get('institution')
            user.save()

            # Send activation email.
            current_site = get_current_site(request)
            mail_subject = 'Active su cuenta en PictoCal.'
            message = render_to_string('authentication/activate_account_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form_user.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'EXITO: Se ha enviado un correo para que active su cuenta.')
            return redirect('login')
    else:
        form_user = RegisterUserForm()
        form_therapist = TherapistForm()

    context = {
        'form_user': form_user,
        'form_therapist': form_therapist
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
            form_user = UserForm(request.POST, instance=user)
            form_therapist = TherapistForm(request.POST, instance=user.therapist)
        if form_user.is_valid() and form_therapist.is_valid():
            form_user.save()
            form_therapist.save()
            return redirect('user-detail', user.id)

    else:
        form_user = UserForm(instance=user)
        form_therapist = TherapistForm(instance=user.therapist)

    context = {
        'form_user': form_user,
        'form_therapist': form_therapist
    }
    return render(request, 'user_data/update_user.html', context)


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, "EXITO! Su cuenta ha sido activada.")

    else:
        messages.error(request, "ERROR! El enlace de activación no es válido.")

    return redirect('login')
