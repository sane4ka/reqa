from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField('Mail', unique=True)
    theoretical_level = models.CharField(max_length=128)
    practical_level = models.CharField(max_length=128)
    is_staff = models.BooleanField()
    is_student = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = AccountManager()

    def __unicode__(self):
        return '%s' % self.email


class Answer(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('tasks.Question', on_delete=models.PROTECT)
