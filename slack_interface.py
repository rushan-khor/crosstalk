import os

import requests
from werkzeug import exceptions

from slack_payload_formatter import plain_message_payload, thumbnail_message_payload, download_button_message_payload

SLACK_BOT_WEBHOOK = os.environ['SLACK_BOT_WEBHOOK']


def send_single_message(context, text=None, thumbnail_url=None, download_url=None):
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


def send_multiple_downloads_message(context, text, multiple_downloads_urls):
    send_single_message(context=context, text=text, thumbnail_url=multiple_downloads_urls[1])
    # send_single_message(context='Next photo', thumbnail_url=multiple_downloads_urls[0])
