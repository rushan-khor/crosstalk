from crosstalk_slack_bot import send_message


def handle_update(update):
    send_message(update['message']['text'])
