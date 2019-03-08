from slack_message_sender import send_message
from tele_user_intent_parser import get_user_intent
from tele_message_parser import get_message_text, make_thumbnail_url_or_none, make_download_button_url_or_none


def forward_message(message, is_edited=False):
    if 'from' not in message:
        raise KeyError(f'No sender info found in Telegram message {message}.')

    user_intent = get_user_intent(message=message, is_edited=is_edited)
    message_text = get_message_text(message)

    thumbnail_url = make_thumbnail_url_or_none(message)
    download_url = make_download_button_url_or_none(message)

    send_message(context=user_intent, text=message_text, thumbnail_url=thumbnail_url, download_url=download_url)


def forward_edited_message(message):
    forward_message(message=message, is_edited=True)
