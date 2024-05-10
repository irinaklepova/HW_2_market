import secrets

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfilaForm, RecoveryForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class ProfileView(UpdateView):
    model = User
    form_class = UserProfilaForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class PasswordRecovery(TemplateView):
    model = User
    template_name = 'users/password_recovery_form.html'
    form_class = RecoveryForm

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return HttpResponse('Пользователя с таким email не существует!')
        new_pass = User.objects.make_random_password()
        user.set_password(new_pass)
        user.save()

        send_mail(
            subject='Вы запросили сброс пароля',
            message=f'Ваш новый пароль {new_pass}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return HttpResponseRedirect(reverse('users:login'))


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
