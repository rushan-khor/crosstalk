import os

import requests
from werkzeug import exceptions

SLACK_BOT_WEBHOOK = os.environ['SLACK_BOT_WEBHOOK']


def send_message(context, text=None, thumbnail_url=None, download_url=None):
    if not text:
        text = ' '

    if thumbnail_url:
        payload = thumbnail_message_payload(context=context, text=text, thumbnail_url=thumbnail_url)
    elif download_url:
        payload = download_button_message_payload(context=context, text=text, download_url=download_url)
    else:
        payload = plain_message_payload(context=context, text=text)

    r = requests.post(SLACK_BOT_WEBHOOK, json=payload)

    if r.status_code != 200 or r.text != 'ok':
        raise exceptions.InternalServerError(r.text)


def plain_message_payload(context, text):
    return {
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
                    "text": text,
                }
            },
        ]
    }


def thumbnail_message_payload(context, text, thumbnail_url):
    return {
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
                    "text": text
                },
                "accessory": {
                    "type": "image",
                    "image_url": thumbnail_url,
                    "alt_text": text
                }
            },
        ]
    }


def download_button_message_payload(context, text, download_url):
    return {
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
                    "text": text
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Download File",
                    },
                    "url": download_url,
                }
            }
        ]
    }
