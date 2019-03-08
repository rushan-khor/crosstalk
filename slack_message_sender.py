import os

import requests
from werkzeug import exceptions

from slack_payload_formatter import thumbnail_message_payload, download_button_message_payload, plain_message_payload

SLACK_APP_WEBHOOK = os.environ['SLACK_APP_WEBHOOK']
BLANK_TEXT_FILLER = ' '


def send_message(context, text=None, thumbnail_url=None, download_url=None):
    if not text:
        text = BLANK_TEXT_FILLER

    if thumbnail_url:
        payload = thumbnail_message_payload(context=context, text=text, thumbnail_url=thumbnail_url)
    elif download_url:
        payload = download_button_message_payload(context=context, text=text, download_url=download_url)
    else:
        payload = plain_message_payload(context=context, text=text)

    r = requests.post(SLACK_APP_WEBHOOK, json=payload)

    if r.status_code != 200 or r.text != 'ok':
        raise exceptions.InternalServerError('Slack API returned an error:', r.text)
