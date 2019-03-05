import os

from flask import Flask, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES

from crosstalk_telegram_bot import handle_update

WEBHOOK_SECRET_KEY = os.environ['TELEGRAM_WEBHOOK_KEY']

app = Flask(__name__)


@app.route("/" + WEBHOOK_SECRET_KEY, methods=['POST'])
def handle_webhook():
    handle_update(update=request.get_json())
    return jsonify({'ok': True})


@app.errorhandler(Exception)
def handle_error(error):
    if not error.code:
        error.code = 500

    if not error.description:
        error.description = str(error)

    return jsonify({
        'ok': False,
        'error_code': error.code,
        'error_reason_phrase': HTTP_STATUS_CODES[error.code],
        'error_description': error.description
    }), error.code
