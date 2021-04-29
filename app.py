# coding: utf-8
from __future__ import unicode_literals
from utils import db
from utils import handler

import json
import logging

from flask import Flask, request
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    conn = db.connect()

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    dialog_handler(request.json, response, conn)

    logging.info('Response: %r', response)
    conn.close()

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def dialog_handler(req, res, conn):
    user_id = req['user']['user_id']

    if req['session']['new']:
        handler.session_new_handler(res, conn, user_id)

    elif req['buttons']['payload'] == 'del_all' or req['request']['nlu']['intents']['del_all_items']:
        db.del_items(conn, user_id, all=True)
        res['response']['text'] = 'Список покупок пуст!'

    else:
        res['response']['text'] = 'Кайф!'

    return
