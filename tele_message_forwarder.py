from slack_interface import send_single_message, send_multiple_downloads_message
from tele_user_intent_parser import get_user_intent
from tele_message_parser import get_message_text, get_message_thumbnail_url, get_message_download_button_url, \
    get_message_multiple_downloads_urls


def forward_message(message, is_edited=False):
    if 'from' not in message:
        raise KeyError(f'No sender info found in Telegram message {message}.')

    user_intent = get_user_intent(message=message, is_edited=is_edited)
    message_text = get_message_text(message)

    thumbnail_url = get_message_thumbnail_url(message)
    download_url = get_message_download_button_url(message)
    multiple_downloads_urls = get_message_multiple_downloads_urls(message)

    if not multiple_downloads_urls:
        send_single_message(context=user_intent, text=message_text, thumbnail_url=thumbnail_url,
                            download_url=download_url)
    else:
        send_multiple_downloads_message(context=user_intent, text=message_text,
                                        multiple_downloads_urls=multiple_downloads_urls)


def forward_edited_message(message):
    forward_message(message=message, is_edited=True)
