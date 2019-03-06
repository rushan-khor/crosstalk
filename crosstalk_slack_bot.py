import os

import requests

SLACK_BOT_WEBHOOK = os.environ['SLACK_BOT_WEBHOOK']


def send_message(from_user, text):
    payload = {
        "text": text,
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f":speech_balloon: _{from_user} says:_"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text,
                }
            },
        ]
    }
    r = requests.post(SLACK_BOT_WEBHOOK, json=payload)  # r.text will be 'ok'
