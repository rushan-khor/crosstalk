from crosstalk_slack_bot import send_message


def handle_update(update):
    message = update['message'] or update['edited_message']
    text = message['text']
    user = message['from']['first_name']
    send_message(from_user=user, text=text)
