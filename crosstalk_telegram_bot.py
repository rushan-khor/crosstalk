from os import environ

import requests

from crosstalk_slack_bot import send_single_message, send_multiple_downloads_message

DEBUG_MODE = environ['DEBUG_MODE'] == 'True'

TELEGRAM_BASE_URL = 'https://api.telegram.org'
BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_API_BASE_URL = f'{TELEGRAM_BASE_URL}/bot{BOT_TOKEN}/'
TELEGRAM_API_BASE_FILE_URL = f'{TELEGRAM_BASE_URL}/file/bot{BOT_TOKEN}/'


def handle_message(message, is_edited=False):
    if DEBUG_MODE:
        print(message)

    if 'from' not in message:
        raise KeyError(f'No from key found in Telegram message {message}.')

    user_intent = get_user_intent(message=message, is_edited=is_edited)
    message_text = get_pretty_message_text(message)

    thumbnail_url = get_message_thumbnail_url(message)
    download_url = get_message_download_button_url(message)
    multiple_downloads_urls = get_message_multiple_downloads_urls(message)

    if not multiple_downloads_urls:
        send_single_message(context=user_intent, text=message_text, thumbnail_url=thumbnail_url,
                            download_url=download_url)
    else:
        send_multiple_downloads_message(context=user_intent, text=message_text,
                                        multiple_downloads_urls=multiple_downloads_urls)


def handle_edited_message(message):
    handle_message(message=message, is_edited=True)


def get_user_intent(message, is_edited=False):
    if is_edited:
        return get_edited_message_user_intent(message)
    elif 'reply_to_message' in message:
        return get_reply_message_user_intent(message)
    elif 'forward_from' in message:
        return get_forwarded_message_user_intent(message)
    else:
        return get_original_message_user_intent(message)


def get_edited_message_user_intent(message):
    from_user = message['from']['first_name']
    return f':pencil2: _{from_user} edited a message to say_:'


def get_reply_message_user_intent(message):
    preceding_message = message['reply_to_message']

    from_user = message['from']['first_name']
    preceding_user = preceding_message['from'].get('first_name', 'an unknown user')

    if preceding_user == from_user:
        preceding_user = 'their own'
    else:
        preceding_user += '\'s'

    preceding_message_type = get_pretty_message_type(preceding_message)

    if preceding_message_type == 'sticker':
        preceding_text = preceding_message['sticker']['emoji']
    else:
        preceding_text = get_message_text_or_caption(preceding_message)

        if not preceding_text:
            return (f':mailbox: _{from_user} '
                    f'replied to {preceding_user} {preceding_message_type}_:')
        elif len(preceding_text) > 20:
            preceding_text = preceding_text[0:19] + '...'

    return (f':mailbox: _{from_user} '
            f'replied to {preceding_user} {preceding_message_type} '
            f'"{preceding_text}"_:')


def get_forwarded_message_user_intent(message):
    from_user = message['from']['first_name']
    preceding_user = message['forward_from'].get('first_name', 'an unknown user')

    if preceding_user == from_user:
        preceding_user = 'their own'
    else:
        preceding_user += '\'s'

    return f':arrow_right: _{from_user} forwarded {preceding_user} message_:'


def get_original_message_user_intent(message):
    from_user = message['from']['first_name']
    message_type = get_pretty_message_type(message)

    if get_pretty_message_text(message) == '/start':
        return f':zap: _{from_user} has started using Crosstalk!_'
    elif message.get('group_chat_created', False):
        new_group_name = message['chat']['title']
        return f':cookie: _{from_user} has created a new group called "{new_group_name}"!_'
    elif message.get('left_chat_member', False):
        left_user = message['left_chat_member']['first_name']
        if left_user == from_user:
            left_user = 'themself'
        return f':wave: _{from_user} has removed {left_user} from the group._'
    elif message.get('new_chat_members', False):
        try:
            new_member_name = message['new_chat_member']['first_name']
        except KeyError:
            new_member_name = 'new members'
        return f':hugging_face: _{from_user} has added {new_member_name} to the group!_'
    elif message_type == 'message':
        return f':speech_balloon: _{from_user} says:_'
    elif message_type == 'photo':
        return f':cityscape: _{from_user} sent a {message_type}:_'
    elif message_type == 'photos':
        return f':world_map: _{from_user} sent a couple of {message_type}:_'
    elif message_type == 'audio clip' or message_type == 'voice recording':
        return f':microphone: _{from_user} sent a {message_type}:_'
    elif message_type == 'video' or message_type == 'video note':
        return f':clapper: _{from_user} sent a {message_type}:_'
    elif message_type == 'sticker':
        return f':fire: _{from_user} sent a {message_type}:_'
    else:
        return f':page_facing_up: _{from_user} sent a {message_type}:_'


def get_pretty_message_text(message):
    if get_message_type(message) == 'sticker':
        return message['sticker'].get('emoji') or '🔥'

    return get_message_text_or_caption(message)


def get_message_text_or_caption(message):
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
    message_type = get_message_type(message)
    valid_message_types = 'audio document video voice video_note contact'.split()

    if message_type in valid_message_types:
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
    api_url = TELEGRAM_API_BASE_URL + 'getFile'
    r = requests.get(api_url, json={'file_id': file_id})

    try:
        data = r.json()
        file_path = data['result']['file_path']
    except ValueError:
        raise ValueError(f'Invalid file ID: {file_id}.')
    except KeyError:
        raise KeyError(f'No file path provided for file ID: {file_id}.')

    return TELEGRAM_API_BASE_FILE_URL + file_path


def get_pretty_message_type(message):
    message_type = get_message_type(message)

    if message_type == 'photo':
        return 'photos'
    elif message_type == 'audio':
        return 'audio clip'
    elif message_type == 'voice':
        return 'voice recording'
    elif message_is_single_photo_type(message):
        return 'photo'

    return message_type.replace('_', ' ')


def get_message_type(message):
    if message.get('audio'):
        return 'audio'
    elif message.get('document'):
        return 'document'
    elif message.get('animation'):
        pass
    elif message.get('game'):
        pass
    elif message.get('photo'):
        return 'photo'
    elif message.get('sticker'):
        return 'sticker'
    elif message.get('video'):
        return 'video'
    elif message.get('voice'):
        return 'voice'
    elif message.get('video_note'):
        return 'video_note'
    elif message.get('contact'):
        return 'contact'
    elif message.get('location'):
        return 'location'
    elif message.get('venue'):
        pass
    elif message.get('invoice'):
        pass
    elif message.get('successful_payment'):
        pass
    return 'message'
