# coding: utf-8
from __future__ import unicode_literals

import pymorphy2
import json
import logging
from flask import Flask, request
from nltk.corpus import stopwords

from utils import db
from utils import handler
from utils import parser


morph = pymorphy2.MorphAnalyzer()

stop_words = stopwords.words("russian")
stop_words.extend(['добавь', 'список', 'продуктов', 'продукты', 'продукт', 'другую', 'ещё', 'другая', 'купить'])


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
    user_id = req['session']['user']['user_id']

    # новая сессия
    if req['session']['new']:
        handler.session_new_handler(res, conn, user_id)

    # очистить список
    elif req.get('buttons', {}).get('payload') == 'del_all' or req['request']['nlu']['intents'].get('del_all_items'):
        db.del_items(conn, user_id, all=True)
        res['response']['text'] = 'Ваш список покупок теперь пуст!'

    # добавить продукты
    elif list(req['request']['nlu']['intents'].keys())[0] == "add_items_nltk":  # TODO: "add_items"
        products, quantities = parser.add_items_parser()
        db.add_items(conn, user_id, products, quantities)
        res['response']['text'] = 'Вот что сейчас в вашем списке покупок.'

    else:
        res['response']['text'] = 'Кайф!'

    return
