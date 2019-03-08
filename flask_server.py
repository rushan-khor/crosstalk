from logging import StreamHandler
from os import environ

from werkzeug import http, exceptions
from flask import Flask, jsonify, request

from tele_message_forwarder import forward_message, forward_edited_message

TELE_WEBHOOK_ENDPOINT = environ['TELEGRAM_WEBHOOK_SECRET']

app = Flask(__name__)
app.logger.addHandler(StreamHandler())


@app.route("/" + TELE_WEBHOOK_ENDPOINT, methods=['POST'])
def handle_telegram_webhook():
    try:
        update = request.get_json(force=True)

        app.logger.info(f'New Telegram update {update}')
        handle_telegram_update(update)

    except exceptions.BadRequest:
        raise exceptions.BadRequest('No JSON found in Telegram update.')

    return jsonify({'ok': True})


def handle_telegram_update(update):
    if 'message' in update:
        forward_message(message=update['message'])
    elif 'edited_message' in update:
        forward_edited_message(message=update['edited_message'])
    else:
        raise KeyError(f'No message found in Telegram update {update}.')


@app.errorhandler(Exception)
def handle_all_exceptions(unknown_exception):
    is_http_exception = isinstance(unknown_exception, exceptions.HTTPException)

    if is_http_exception:
        http_exception = unknown_exception
    else:
        builtin_exception_description = f'{type(unknown_exception).__name__}: {str(unknown_exception)}'
        http_exception = exceptions.InternalServerError(description=builtin_exception_description)

    is_in_debug_mode = environ['FLASK_ENV'] == 'development'

    app.logger.error(
        f'<{http_exception.code} '
        f'{http.HTTP_STATUS_CODES[http_exception.code]}> '
        f'{http_exception.description}',
        exc_info=1 if is_in_debug_mode else 0
    )

    return jsonify({'ok': True})
