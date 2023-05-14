import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from accounts.models import Answer, Account
from jira_tasks.api import JiraAPIClient

from .models import Question, TheoreticalTask, PracticalTask, JiraIssue
from .tasks import send_feedback_task


class QuestionView(View):

    def _get_incorrect_answers(self, request):
        incorrect_answers = Answer.objects.filter(question__type='start', is_correct=False,
                                                  account=request.user).order_by('-id')
        modules = [x.question.module for x in incorrect_answers]
        context = dict(finished=True, modules=modules)
        return render(request, 'tasks/question.html', context=context)

    def get(self, request):
        last_answer = Answer.objects.filter(question__type='start', account=request.user).order_by('-id').first()
        if not last_answer:
            question = Question.objects.filter(type='start').order_by('order').prefetch_related('answers').first()
        else:
            question = Question.objects.filter(type='start', order=last_answer.question.order + 1)\
                .prefetch_related('answers').first()
            if not question:
                return self._get_incorrect_answers(request)
        return render(request, 'tasks/question.html', context=dict(finished=False, question=question))

    def post(self, request):
        question_id = request.POST.get('question-id')

        question = Question.objects.get(id=question_id)
        answer = request.POST.get('option')
        Answer.objects.create(account=request.user, answer=answer, question=question,
                              is_correct=answer == question.correct_answer)
        next_question = Question.objects.filter(type='start', order=question.order + 1).prefetch_related('answers').\
            first()
        if not next_question:
            return self._get_incorrect_answers(request)
        return render(request, 'tasks/question.html', context=dict(finished=False, question=next_question))


class JiraTasks:

    def __init__(self):
        self.jira = JiraAPIClient()

    def get_jira_user_id(self, user):
        result = self.jira.search_user(user.email)
        return result['accountId']

    def init_study(self, user):
        if JiraIssue.objects.filter(account=user).exists():
            raise ValueError('Study already started')
        user_id = self.get_jira_user_id(user)
        theory_task = TheoreticalTask.objects.filter(module__order=0).first()
        practical_task = PracticalTask.objects.filter(module__order=0).first()
        result1 = self.jira.create_issue(theory_task.name, f'{theory_task.description}: {theory_task.url}')
        result2 = self.jira.create_issue(practical_task.name, practical_task.description)
        JiraIssue.objects.create(account=user, theoretical_task=theory_task, jira_issue_id=result1['id'],
                                 jira_key=result1['key'], link=result1['self'])
        JiraIssue.objects.create(account=user, practical_task=practical_task, jira_issue_id=result2['id'],
                                 jira_key=result2['key'], link=result2['self'])
        self.jira.assign_issue(result1['id'], user_id)
        self.jira.assign_issue(result2['id'], user_id)

    def send_next_task(self, user):
        last_issue = JiraIssue.objects.filter(account=user).order_by('-id').first()
        if not last_issue:
            self.init_study(user)
        user_id = self.get_jira_user_id(user)
        theory_task = TheoreticalTask.objects.filter(module__order=0).first()
        practical_task = PracticalTask.objects.filter(module__order=0).first()
        result1 = self.jira.create_issue(theory_task.name, f'{theory_task.description}: {theory_task.url}')
        result2 = self.jira.create_issue(practical_task.name, practical_task.description)
        JiraIssue.objects.create(account=user, theoretical_task=theory_task, jira_issue_id=result1['id'],
                                 jira_key=result1['key'], link=result1['self'])
        JiraIssue.objects.create(account=user, practical_task=practical_task, jira_issue_id=result2['id'],
                                 jira_key=result2['key'], link=result2['self'])
        self.jira.assign_issue(result1['id'], user_id)
        self.jira.assign_issue(result2['id'], user_id)


def start_study(request):
    jira_tasks = JiraTasks()
    jira_tasks.init_study(request.user)
    return render(request, 'tasks/starting.html')


def send_tasks(request, pk):
    user = Account.objects.get(id=pk)
    jira_tasks = JiraTasks()
    jira_tasks.send_next_task(user)
    return render(request, 'tasks/tasks.html')


@csrf_exempt
def jira_webhook(request):
    data = json.loads(request.body)
    webhook_event = data['webhookEvent']
    if webhook_event == 'comment_created':
        comment = data['comment']['body']
        issue_id = data['issue']['id']
        jira_task = JiraIssue.objects.filter(jira_issue_id=issue_id).first()
        if jira_task and jira_task.practical_task and not jira_task.chat_gpt_comment:
            send_feedback_task.delay(jira_task.id, comment)

    return JsonResponse({})
