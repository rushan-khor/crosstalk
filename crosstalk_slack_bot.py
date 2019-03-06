import os

import requests

SLACK_BOT_WEBHOOK = os.environ['SLACK_BOT_WEBHOOK']


def send_message(user_intent):
    payload = {
        "text": user_intent,
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": user_intent
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": user_intent,
                }
            },
        ]
    }
    r = requests.post(SLACK_BOT_WEBHOOK, json=payload)  # r.text will be 'ok'
