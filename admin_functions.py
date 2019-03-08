import os
import random
import string

import requests

BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_API_HOSTNAME = os.environ['TELEGRAM_API_HOSTNAME']
TELEGRAM_BOT_API_URL = f'{TELEGRAM_API_HOSTNAME}bot{BOT_TOKEN}/'

TELEGRAM_WEBHOOK_SECRET = os.environ['TELEGRAM_WEBHOOK_SECRET']
TELEGRAM_WEBHOOK_URL = os.environ['TELEGRAM_WEBHOOK_HOSTNAME'] + TELEGRAM_WEBHOOK_SECRET

CONSOLE_TITLE_DIVIDER = '\n'
CONSOLE_LINE_INDENT = '* '


def set_webhook():
    r = requests.post(TELEGRAM_BOT_API_URL + 'setWebhook', json={'url': TELEGRAM_WEBHOOK_URL})
    result = r.json()
    return str(result)


def delete_webhook():
    r = requests.get(TELEGRAM_BOT_API_URL + 'deleteWebhook')
    result = r.json()
    return str(result)


def get_webhook_info():
    r = requests.get(TELEGRAM_BOT_API_URL + 'getWebhookInfo')
    result = r.json()
    return str(result)


def generate_secret_key():
    candidate_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    chosen_characters = random.sample(candidate_characters, 32)
    new_key = ''.join(chosen_characters)
    return new_key


if __name__ == '__main__':
    print(CONSOLE_TITLE_DIVIDER + 'TELEGRAM BOT ADMIN')
    print(CONSOLE_LINE_INDENT + 'Telegram bot token:\t' + BOT_TOKEN)
    print(CONSOLE_LINE_INDENT + 'Telegram API URL:\t\t' + TELEGRAM_BOT_API_URL)

    print(CONSOLE_TITLE_DIVIDER + 'WEBHOOK ADMIN')
    print(CONSOLE_LINE_INDENT + 'Webhook secret key:\t\t' + TELEGRAM_WEBHOOK_URL)
    print(CONSOLE_LINE_INDENT + 'Webhook URL:\t\t\t\t' + TELEGRAM_WEBHOOK_URL)
    # print(CONSOLE_LINE_INDENT + 'Set Webhook response:\t\t' + set_webhook())
    # print(CONSOLE_LINE_INDENT + 'Delete Debhook response:\t' + delete_webhook())
    print(CONSOLE_LINE_INDENT + 'Webhook Info response:\t' + get_webhook_info())
    # print(CONSOLE_LINE_INDENT + 'New key generated:\t\t' + generate_secret_key())
