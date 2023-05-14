from reqa.celery import app as celery_app
from chat.chat_gpt import ChatGPTAPI
from tasks.models import JiraIssue
from jira_tasks.api import JiraAPIClient


@celery_app.task()
def send_feedback_task(jira_issue_id, comment):
    jira_task = JiraIssue.objects.get(id=jira_issue_id)
    chat = ChatGPTAPI()
    response = chat.request_feedback(jira_task.practical_task.description, comment)
    jira_task.chat_gpt_comment = response
    jira_task.save()
    jira = JiraAPIClient()
    jira.create_comment(jira_task.jira_issue_id, response)
