import json

import requests
from requests.auth import HTTPBasicAuth

from logging import getLogger


class JiraRestAPIClientException(Exception):
    pass


logger = getLogger(__name__)


class JiraAPIClient:
    def __init__(self):
        self.api_token = 'ATATT3xFfGF04sRmaJhaQFTqcLA3cNHFtbkrnNJPF5fsrlYUkTncVz21LMp39Ap1-WmdK9QLCAIXEYtgs2bRa8pzBQUg-2SJFsN6oInme4R5Btv5YxSMMKHdFEEgQ548sYoYBzpPYLfb5lniqT2Cciky65coOhbERd74kraWz5kd8065nzLHo-k=5D0F2274'
        self.api_url = 'https://reqa.atlassian.net/rest/api/3'

    @property
    def default_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    @property
    def auth(self):
        return HTTPBasicAuth("sane4ka.sh@gmail.com", self.api_token)

    @staticmethod
    def _get_payload(summary, description):
        return {
            'fields': {
                'project': {
                    'key': 'QT'
                },
                'summary': summary,
                'description': {
                    "content": [
                        {
                            "content": [
                                {
                                    "text": description,
                                    "type": "text"
                                }
                            ],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                'issuetype': {
                    'id': '10004'
                },
            }
        }

    def create_issue(self, summary, description):
        payload = self._get_payload(summary, description)
        response = requests.post(self.api_url + '/issue', headers=self.default_headers, json=payload, auth=self.auth)
        if response.status_code != 201:
            logger.warning(f'Error while creating new project in JIRA. Detail: {response.text}')
            raise JiraRestAPIClientException('Error while creating project in JIRA')
        return response.json()

    def create_comment(self, issue_id, comment):
        payload = {
          "body": {
            "content": [
              {
                "content": [
                  {
                    "text": comment,
                    "type": "text"
                  }
                ],
                "type": "paragraph"
              }
            ],
            "type": "doc",
            "version": 1
          }
        }
        response = requests.post(self.api_url + f'/issue/{issue_id}/comment', headers=self.default_headers,
                                 json=payload, auth=self.auth)
        return response

    def assign_issue(self, issue_id, user_id):
        payload = dict(accountId=user_id)
        response = requests.put(self.api_url + f'/issue/{issue_id}/assignee', headers=self.default_headers,
                                json=payload, auth=self.auth)
        return response

    def search_user(self, email):
        response = requests.get(self.api_url + f'/user/search?query={email}', headers=self.default_headers,
                                auth=self.auth)
        return response.json()[0]

    def get_issue_by_code(self, issue_code: str):
        response = requests.get(self.api_url + f'/issue/{issue_code}', headers=self.default_headers, auth=self.auth)
        if response.status_code != 200:
            return False
        return response.json()

    def update_issue_data(self, issue_code: str, payload: json.dumps):
        api_url = 'https://reqa.atlassian.net/rest/api/2'
        response = requests.put(api_url + f'/issue/{issue_code}', headers=self.default_headers, auth=self.auth,
                                data=payload)
        if response.status_code != 204:
            logger.warning(f'Error while updating issue: {issue_code}. Error text: {response.text}')
            raise JiraRestAPIClientException('Error while updating project in JIRA')
        return response
