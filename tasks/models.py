from django.db import models

from accounts.models import Account


class QALevel(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    qa_level = models.ForeignKey(QALevel, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name}, level {self.qa_level.name}'


class TheoreticalTask(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.module.name}'


class PracticalTask(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    maximum_rank = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}, {self.module.name}'


class Question(models.Model):
    type = models.CharField(max_length=64, default='start')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    question = models.TextField()
    order = models.PositiveIntegerField(default=0)
    correct_answer = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.module.name}, question {self.order}'


class AnswerVariant(models.Model):
    code = models.CharField(max_length=2)
    answer = models.CharField(max_length=128)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f'{self.question.question}, {self.code}, question {self.answer}'


class JiraIssue(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    jira_issue_id = models.PositiveIntegerField()
    jira_key = models.CharField(max_length=64)
    link = models.URLField()
    theoretical_task = models.ForeignKey(TheoreticalTask, null=True, on_delete=models.PROTECT)
    practical_task = models.ForeignKey(PracticalTask, null=True, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    chat_gpt_rank = models.PositiveIntegerField(null=True)
    chat_gpt_comment = models.TextField(null=True)
