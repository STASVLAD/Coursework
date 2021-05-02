# coding: utf-8
from __future__ import unicode_literals

import pymorphy2
import json
import logging
from flask import Flask, request
from nltk.corpus import stopwords

from utils import db
from utils import response
from utils import parser

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

morph = pymorphy2.MorphAnalyzer()


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
        response.session_new_response(res, conn, user_id)

    # очистить список
    elif req.get('buttons', {}).get('payload') == 'del_all' or req['request']['nlu']['intents'].get('del_all_items'):
        db.del_items(conn, user_id, all=True)
        res['response']['text'] = 'Ваш список покупок теперь пуст!'

    # добавить продукты
    elif list(req['request']['nlu']['intents'].keys())[0] == "add_items_nltk":  # TODO: "add_items"
        tokens = req['request']['nlu']['tokes']
        intent_start = req['request']['nlu']['intents']['add_items_nltk']['slots']['food']['tokens']['start']
        intent_end = req['request']['nlu']['intents']['add_items_nltk']['slots']['food']['tokens']['end']

        gr_i = parser.gramma_info(morph, tokens, intent_start, intent_end)
        products, quantities, units = parser.tokens_parser(gr_i)  # TODO: "units"
        db.add_items(conn, user_id, products, quantities)
        response.add_items_response(conn, user_id, products, quantities)

    elif list(req['request']['nlu']['intents'].keys())[0] == "del_items":
        tokens = req['request']['nlu']['tokes']
        intent_start = req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['start']
        intent_end = req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['end']

        gr_i = parser.gramma_info(morph,    tokens, intent_start, intent_end)
        products, quantities, units = parser.tokens_parser(gr_i)  # TODO: "units"
        db.dell_items(conn, user_id, products, quantities)
        response.del_items_response(conn, user_id, products, quantities)

    else:
        res['response']['text'] = 'Кайф!'

    return
