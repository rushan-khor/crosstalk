import os
import random
import string

import requests

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

WEBHOOK_SECRET_KEY = os.environ['TELEGRAM_WEBHOOK_KEY']
WEBHOOK_URL = os.environ['TELEGRAM_WEBHOOK_HOSTNAME'] + WEBHOOK_SECRET_KEY

CONSOLE_TITLE_DIVIDER = '\n'
CONSOLE_LINE_INDENT = '* '


def set_webhook():
    r = requests.get(TELEGRAM_API_URL + 'setWebhook', json={'url': WEBHOOK_URL})
    result = r.json()
    return str(result)


def delete_webhook():
    r = requests.get(TELEGRAM_API_URL + 'deleteWebhook')
    result = r.json()
    return str(result)


def get_webhook_info():
    r = requests.get(TELEGRAM_API_URL + 'getWebhookInfo')
    result = r.json()
    return str(result)


def generate_secret_key():
    candidate_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    chosen_characters = random.sample(candidate_characters, 32)
    new_key = ''.join(chosen_characters)
    return new_key


if __name__ == '__main__':
    print(CONSOLE_TITLE_DIVIDER + 'TELEGRAM BOT ADMIN')
    print(CONSOLE_LINE_INDENT + 'Telegram bot token:\t' + TOKEN)
    print(CONSOLE_LINE_INDENT + 'Telegram API URL:\t\t' + TELEGRAM_API_URL)

    print(CONSOLE_TITLE_DIVIDER + 'WEBHOOK ADMIN')
    print(CONSOLE_LINE_INDENT + 'Webhook secret key:\t\t' + WEBHOOK_SECRET_KEY)
    print(CONSOLE_LINE_INDENT + 'Webhook URL:\t\t\t\t' + WEBHOOK_URL)
    # print(CONSOLE_LINE_INDENT + 'Set Webhook response:\t\t' + set_webhook())
    # print(CONSOLE_LINE_INDENT + 'Delete Debhook response:\t' + delete_webhook())
    print(CONSOLE_LINE_INDENT + 'Webhook Info response:\t' + get_webhook_info())
    # print(CONSOLE_LINE_INDENT + 'New key generated:\t\t' + generate_secret_key())
