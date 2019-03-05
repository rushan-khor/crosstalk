import os

from flask import Flask, jsonify, request
from werkzeug.http import HTTP_STATUS_CODES

WEBHOOK_SECRET_KEY = os.environ['WEBHOOK_SECRET_KEY']

app = Flask(__name__)


@app.route("/" + WEBHOOK_SECRET_KEY, methods=['POST'])
def handle_webhook():
    print(request)
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
        'reason_phrase': HTTP_STATUS_CODES[error.code],
        'description': error.description
    }), error.code