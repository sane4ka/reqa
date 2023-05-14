from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import TemplateView


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'


class TestDescriptionView(TemplateView):
    template_name = 'accounts/test_description.html'


def registration(request):
    pass