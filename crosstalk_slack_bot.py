import os

import requests

SLACK_BOT_WEBHOOK = os.environ['SLACK_BOT_WEBHOOK']


def send_message(text):
    r = requests.post(SLACK_BOT_WEBHOOK, json={'text': text})  # r.text will be 'ok'
