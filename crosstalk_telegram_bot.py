from crosstalk_slack_bot import send_message

DEBUG_MODE = True
BLANK_MESSAGE_PLACEHOLDER = ' '


def handle_message(message, is_edited=False):
    if DEBUG_MODE:
        print(message)

    if 'from' not in message:
        raise KeyError(f'No from key found in Telegram message {message}.')
    else:
        user_intent = get_user_intent(message=message, is_edited=is_edited)

    send_message(user_intent)


def handle_edited_message(message):
    handle_message(message=message, is_edited=True)


def get_user_intent(message, is_edited=False):
    from_user_display_name = message['from']['first_name']

    if is_edited:
        return f':pencil2: _{from_user_display_name} edited a message to say_:'
    elif 'reply_to_message' in message:
        preceding_message = message['reply_to_message']

        preceding_user = preceding_message['from'].get('first_name', 'an unknown user')
        preceding_message_type = get_message_content_type(preceding_message).replace('_', ' ')
        preceding_text = get_message_text_or_caption(preceding_message)

        if len(preceding_text) > 20:
            preceding_text = preceding_text[0:19] + '...'

        if preceding_text is BLANK_MESSAGE_PLACEHOLDER:
            return (f':mailbox: _{from_user_display_name} '
                    f'replied to {preceding_user}\'s {preceding_message_type}_:')
        else:
            return (f':mailbox: _{from_user_display_name} '
                    f'replied to {preceding_user}\'s {preceding_message_type} '
                    f'"{preceding_text}"_:')
    elif 'forward_from' in message:
        preceding_user = message['forward_from'].get('first_name', 'an unknown user')
        return f':arrow_right: _{from_user_display_name} forwarded {preceding_user}\'s message_:'
    else:
        return f':speech_balloon: _{from_user_display_name} says_:'


def get_message_text_or_caption(message):
    return message.get('text') or message.get('caption') or BLANK_MESSAGE_PLACEHOLDER


def get_message_content_type(message):
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
