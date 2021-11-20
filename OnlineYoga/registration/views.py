from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string

from .forms import LoginForm, RegisterForm

# Create your views here.
class LandingpageView(TemplateView):
    template_name = "registration/landingpage.html"


class Login(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = "registration/landingpage.html"


User = get_user_model()

class Register(CreateView):
    template_name = "registration/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            "protocol": self.request.scheme,
            "domain": domain,
            "token": dumps(user.pk),
            "user": user,
        }

        subject = render_to_string("registration/mail_template/create/subject.txt", context)
        message = render_to_string("registration/mail_template/create/message.txt", context)
        from_email = "cocoyoga@ihciad.com"

        user.email_user(subject, message, from_email)
        return redirect("register_done")


class RegisterDone(TemplateView):
    template_name = "registration/register_done.html"


class RegisterComplete(TemplateView):
    template_name = "registration/register_complete.html"
    timeout_seconds = getattr(settings, "ACTIVATION_TIMEOUT_SECONDS", 60*60*24)

    def get(self, request, **kwargs):
        token = kwargs.get("token")

        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()