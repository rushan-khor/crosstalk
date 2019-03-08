from os import environ

import requests

API_HOSTNAME = environ['TELEGRAM_API_HOSTNAME']
BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']

BOT_API_BASE_URL = f'{API_HOSTNAME}bot{BOT_TOKEN}/'
BOT_FILE_PATH_BASE_URL = f'{API_HOSTNAME}/file/bot{BOT_TOKEN}/'

MESSAGE_TYPE_CHECK_ORDER = 'document sticker video_note voice audio video photo'.split()
VALID_MESSAGE_TYPES = 'audio document video voice video_note contact'.split()


def get_message_text(message):
    if get_raw_message_type(message) == 'sticker':
        return message['sticker'].get('emoji') or '🔥'

    return get_raw_message_text_or_caption(message)


def get_raw_message_text_or_caption(message):
    return message.get('text') or message.get('caption')


def message_is_single_photo_type(message):
    try:
        photo_mime_type_prefix = 'image/'
        return photo_mime_type_prefix in message['document']['mime_type']
    except KeyError:
        return False


def get_message_thumbnail_url(message):
    try:
        photo_mime_type_prefix = 'image/'

        if photo_mime_type_prefix in message['document']['mime_type']:
            return get_url_from_file_id(message['document']['thumb']['file_id'])
        else:
            return None

    except KeyError:
        return None


def get_message_download_button_url(message):
    message_type = get_raw_message_type(message)

    if message_type in VALID_MESSAGE_TYPES:
        return get_url_from_file_id(message[message_type]['file_id'])
    else:
        return None


def get_message_multiple_downloads_urls(message):
    try:
        photos = message['photo']
    except KeyError:
        return None

    if not isinstance(photos, list):
        return None

    urls = []
    for photo in photos:
        try:
            file_id = photo['file_id']
            urls.append(get_url_from_file_id(file_id))
        except KeyError:
            continue

    return urls


def get_url_from_file_id(file_id):
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


def get_message_type(message):
    raw_type = get_raw_message_type(message)

    if raw_type == 'photo':
        return 'photos'
    elif raw_type == 'audio':
        return 'audio clip'
    elif raw_type == 'voice':
        return 'voice recording'
    elif message_is_single_photo_type(message):
        return 'photo'

    return raw_type.replace('_', ' ')


def get_raw_message_type(message):
    for message_type in MESSAGE_TYPE_CHECK_ORDER:
        if message.get(message_type):
            return message_type

    return 'message'
