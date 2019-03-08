from os import environ

from flask import Flask, jsonify, request
from werkzeug import http, exceptions

from tele_interface import handle_message, handle_edited_message

TELE_WEBHOOK_ENDPOINT = environ['TELE_WEBHOOK_SECRET']

app = Flask(__name__)


@app.route("/" + TELE_WEBHOOK_ENDPOINT, methods=['POST'])
def handle_telegram_webhook():
    try:
        update = request.get_json(force=True)
        handle_telegram_update(update)
    except exceptions.BadRequest:
        raise exceptions.BadRequest('No JSON found in Telegram update.')
    return jsonify({'ok': True})


def handle_telegram_update(update):
    if 'message' in update:
        handle_message(message=update['message'])
    elif 'edited_message' in update:
        handle_edited_message(message=update['edited_message'])
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

    app.logger.error(
        f'<{http_exception.code} '
        f'{http.HTTP_STATUS_CODES[http_exception.code]}> '
        f'{http_exception.description}'
    )

    return jsonify({'ok': True})
