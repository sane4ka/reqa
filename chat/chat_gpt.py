import json
import requests


import logging
logger = logging.getLogger('__name__')


class ChatGPTAPI:
    url = 'https://tonai.tech/api/public/v1/services'
    key = 'reqa_test_key_90284553-6c21-493f-8320-08107225e180'
    prompt = 'Could you verify my answer on this task and rate it from 1 to 10?\nTask:'
    answer_prompt = 'My answer: '

    def services_list(self):
        response = requests.get(self.url, headers=dict(key=self.key))
        return response.json()

    def send_message(self, message):
        data = dict(service_id='6j99xutxsmiwpt6', messages=json.dumps([dict(role='system', content=message)]),
                    temperature=0.6, top_p=0.2, n=1)
        response = requests.post(self.url, json=data, headers=dict(key=self.key))
        if response.status_code != 200:
            logger.error(f'Error response from ChatGPT: {response.status_code} {response.text}')
        return response

    def request_feedback(self, task, answer):
        response = self.send_message(self.prompt + task + self.answer_prompt + answer)
        try:
            data = json.loads(response.text)['messages'][0]['text']
        except KeyError:
            return 'Please give us some more tokens to get feedback.'
        text = json.loads(data)
        return text['choices'][0]['message']['content']
