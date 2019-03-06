from os import environ

from flask import Flask, jsonify, request
from werkzeug import http, exceptions

from crosstalk_telegram_bot import handle_message

WEBHOOK_SECRET_KEY = environ['TELEGRAM_WEBHOOK_KEY']

app = Flask(__name__)


@app.route("/" + WEBHOOK_SECRET_KEY, methods=['POST'])
def handle_webhook():
    try:
        update = request.get_json()
        handle_update(update)
    except exceptions.BadRequest:
        raise exceptions.BadRequest('No JSON found in Flask request.')
    return jsonify({'ok': True})


def handle_update(update=None):
    if 'edited_message' in update:
        handle_message(message=update['message'], is_edited=True)
    elif 'message' in update:
        handle_message(message=update['message'], is_edited=False)

    raise KeyError(f'No message found in Telegram update {update}.')


@app.errorhandler(Exception)
def handle_exception(unknown_exception):
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
