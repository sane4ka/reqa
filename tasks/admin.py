from django.contrib import admin

from .models import TheoreticalTask, PracticalTask, Question, AnswerVariant, Module, QALevel


admin.site.register(TheoreticalTask)
admin.site.register(PracticalTask)
admin.site.register(Question)
admin.site.register(AnswerVariant)
admin.site.register(Module)
admin.site.register(QALevel)

