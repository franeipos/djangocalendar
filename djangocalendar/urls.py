"""djangocalendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # for password reset and change

from django.conf import settings
from django.conf.urls.static import static

from my_calendar.views import (
    home_view,
    calendar_view,
    all_events_view,
    event_detail,
    add_event,
    update_event,
    delete_event,
    search_pictograms,
    pictogram_detail,
    patients_list,
    add_patient,
    update_patient,
    delete_patient,
    calendar_to_pdf,
)

from accounts.views import (
    login_user,
    logout_user,
    register_user,
    user_detail,
    update_user,
    activate_account,
    send_activation_mail
)

urlpatterns = [
                path('admin/', admin.site.urls),
                path('', login_user, name="home"),
                path('calendar/<int:id_patient>/', calendar_view, name="calendar"),
                path('calendar/<int:id_patient>/<int:month>/<int:year>/', calendar_view, name="calendar"),
                path('calendar/event_detail/<int:event_id>/', event_detail, name="event-detail"),
                path('calendar/events/<int:id_patient>', all_events_view, name="events-list"),
                path('calendar/add_event/<int:day>/<int:month>/<int:year>/', add_event, name="add-event"),
                path('calendar/add_event/', add_event, name="add-event"),
                path('calendar/update_event/<int:event_id>/', update_event, name="update-event"),
                path('calendar/delete_event/<int:event_id>/', delete_event, name="delete-event"),
                path('calendar/search_pictograms/', search_pictograms, name="search-pictograms"),
                path('calendar/pictogram/<int:picto_id>', pictogram_detail, name="pictogram-detail"),
                path('calendar/patients/', patients_list, name="patients-list"),
                path('calendar/add_patient/', add_patient, name="add-patient"),
                path('calendar/update_patient/<int:id_patient>/', update_patient, name="update-patient"),
                path('calendar/delete_patient/<int:id_patient>/', delete_patient, name="delete-patient"),
                path('calendar/to_pdf/<int:id_patient>/<int:month>/<int:year>/', calendar_to_pdf,
                   name="calendar-to-pdf"),

                # Account URLs
                path('/accounts/', include('django.contrib.auth.urls')),
                path('accounts/login/', login_user, name="login"),
                path('accounts/logout/', logout_user, name="logout"),
                path('accounts/register_user/', register_user, name="register_user"),
                path('accounts/user_detail/<int:user_id>/', user_detail, name="user-detail"),
                path('accounts/update_user/<int:user_id>/', update_user, name="update-user"),

                # Password reset URLs
                path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
                  template_name='password_reset/password_change_done.html'),
                   name='password_change_done'),

                path('accounts/password_change/',
                   auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
                   name='password_change'),

                path('accounts/password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                  template_name='password_reset/password_reset_done.html'),
                   name='password_reset_done'),

                path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                    template_name='password_reset/password_reset_confirm.html'),
                   name='password_reset_confirm'),

                path('password_reset/', auth_views.PasswordResetView.as_view(
                    template_name='password_reset/password_reset_form.html'),
                     name='password_reset'),

                path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
                  template_name='password_reset/password_reset_complete.html'),
                   name='password_reset_complete'),

                path('accounts/activate_account/<uidb64>/<token>/', activate_account, name='activate-account'),
                path('accounts/send_activation_mail/<int:user_id>/', send_activation_mail, name='send-activation-mail')


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
