from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'tasks'


urlpatterns = [
    path(r'start-test', login_required(views.QuestionView.as_view()), name='start-test-question'),
    path(r'init-test', login_required(views.start_study), name='start-study'),
    path(r'jira/webhook', views.jira_webhook, name='jira-webhook')
]
