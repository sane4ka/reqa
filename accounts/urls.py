from django.urls import path
from . import views


app_name = 'accounts'


urlpatterns = [
    path(r'accounts/login', views.LoginView.as_view(), name='token'),
    path(r'test', views.TestDescriptionView.as_view(), name='token'),
]
