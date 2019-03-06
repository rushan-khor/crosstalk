import os

import requests

SLACK_BOT_WEBHOOK = os.environ['SLACK_BOT_WEBHOOK']


def send_message(context, text=None, photo_url=None, download_url=None):
    payload = {
        "text": context,
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": context
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": context,
                }
            },
        ]
    }
    r = requests.post(SLACK_BOT_WEBHOOK, json=payload)  # r.text will be 'ok'
