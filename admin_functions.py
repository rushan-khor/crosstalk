import os
import random
import string

import requests

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

WEBHOOK_SECRET_KEY = os.environ['WEBHOOK_SECRET_KEY']
WEBHOOK_URL = os.environ['WEBHOOK_HOSTNAME'] + WEBHOOK_SECRET_KEY

CONSOLE_TITLE_DIVIDER = '\n'
CONSOLE_BULLET = '*'


def set_webhook():
    r = requests.post(TELEGRAM_API_URL + 'setWebhook', data={'url': WEBHOOK_URL})
    return r.json()


def delete_webhook():
    r = requests.post(TELEGRAM_API_URL + 'setWebhook', data={'url': ''})
    return r.json()


def generate_secret_key():
    candidate_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    chosen_characters = random.sample(candidate_characters, 32)
    new_key = ''.join(chosen_characters)
    return new_key


if __name__ == '__main__':
    print(CONSOLE_TITLE_DIVIDER + 'TELEGRAM ADMIN')
    print(CONSOLE_BULLET, 'Telegram bot token:\t', TOKEN)
    print(CONSOLE_BULLET, 'Telegram API URL:\t\t', TELEGRAM_API_URL)
    print(CONSOLE_BULLET, 'Webhook secret key:\t', WEBHOOK_SECRET_KEY)
    print(CONSOLE_BULLET, 'Webhook URL:\t\t\t', WEBHOOK_URL)

    print(CONSOLE_TITLE_DIVIDER + 'WEBHOOK ADMIN')
    # print(CONSOLE_BULLET, 'Set webhook response:\t\t', set_webhook())
    # print(CONSOLE_BULLET, 'Delete webhook response:\t', delete_webhook())
    # print(CONSOLE_BULLET, 'New key generated:\t\t', generate_secret_key())