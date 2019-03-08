from os import environ

import requests

API_HOSTNAME = environ['TELEGRAM_API_HOSTNAME']
BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']

BOT_API_BASE_URL = f'{API_HOSTNAME}bot{BOT_TOKEN}/'
BOT_FILE_PATH_BASE_URL = f'{API_HOSTNAME}/file/bot{BOT_TOKEN}/'

RAW_MESSAGE_TYPE_CHECK_ORDER = 'document sticker video_note voice audio video photo'.split()
DOWNLOAD_BUTTON_RAW_MESSAGE_TYPES = 'audio document video voice video_note'.split()


def get_message_type(message):
    raw_type = get_raw_message_type(message)

    if raw_type == 'audio':
        return 'audio clip'
    elif raw_type == 'voice':
        return 'voice recording'
    elif get_thumbnail_file_id(message):
        return 'photo'

    return raw_type.replace('_', ' ')


def get_raw_message_type(message):
    for message_type in RAW_MESSAGE_TYPE_CHECK_ORDER:
        if message.get(message_type):
            return message_type

    return 'message'


def get_message_text(message):
    raw_message_text = get_raw_message_text_or_caption(message)

    if raw_message_text == '/start':
        return ':wave:'
    elif get_raw_message_type(message) == 'sticker':
        return message['sticker'].get('emoji') or '🔥'
    elif get_raw_message_type(message) == 'document':
        file_name = message['document'].get('file_name') or 'Download'
        message_text = raw_message_text or ''
        return f'*:paperclip: {file_name}* {message_text}'

    return get_raw_message_text_or_caption(message)


def get_raw_message_text_or_caption(message):
    return message.get('text') or message.get('caption')


def get_thumbnail_file_id(message):
    try:
        return message['photo'][1]['file_id']
    except KeyError:
        pass

    try:
        photo_mime_type_prefix = 'image/'

        if photo_mime_type_prefix in message['document']['mime_type']:
            return message['document']['thumb']['file_id']
    except KeyError:
        return None


def make_thumbnail_url_or_none(message):
    file_id = get_thumbnail_file_id(message)

    if file_id:
        return make_url_from_file_id(file_id)

    return None


def make_download_button_url_or_none(message):
    message_type = get_raw_message_type(message)

    if message_type in DOWNLOAD_BUTTON_RAW_MESSAGE_TYPES:
        return make_url_from_file_id(message[message_type]['file_id'])
    else:
        return None


def make_url_from_file_id(file_id):
    api_url = BOT_API_BASE_URL + 'getFile'
    r = requests.get(api_url, json={'file_id': file_id})

    try:
        data = r.json()
        file_path = data['result']['file_path']
    except ValueError:
        raise ValueError(f'Invalid file ID: {file_id}.')
    except KeyError:
        raise KeyError(f'No file path provided for file ID: {file_id}.')

    return BOT_FILE_PATH_BASE_URL + file_path
