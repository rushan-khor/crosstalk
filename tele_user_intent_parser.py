from tele_message_parser import get_message_text, get_raw_message_text_or_caption, get_message_type


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

    preceding_message_type = get_message_type(preceding_message)

    if preceding_message_type == 'sticker':
        preceding_text = preceding_message['sticker']['emoji']
    else:
        preceding_text = get_raw_message_text_or_caption(preceding_message)

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
    message_type = get_message_type(message)

    if get_message_text(message) == '/start':
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
