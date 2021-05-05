# coding: utf-8
from __future__ import unicode_literals

import json
import logging
from flask import Flask, request
from nltk.corpus import stopwords

from utils import db
from utils import response
from utils import parser
from utils import config

from pprint import pformat

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
config.init()


@app.route("/", methods=['POST'])
def main():
    logging.info('Request\n' + str(pformat(request.json)))
    conn = db.connect()

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    dialog_handler(request.json, response, conn)

    logging.info('Response\n' + str(pformat(response)))
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
        if not db.is_new_user(conn, user_id):
            res['response']['text'] = 'Описание навыка'  # TODO Описание навыка
        else:
            shopping_list = db.get_items(conn, user_id)
            response.get_items_response(res, shopping_list)
            res['response']['text'] = 'Привет!\n' + res['response']['text']

    # очистить список
    elif req.get('buttons', {}).get('payload') == 'del_all' or req['request']['nlu']['intents'].get('del_all_items'):
        res['response']['text'] = 'Ваш список покупок теперь пуст!'
        db.del_items(conn, user_id, all=True)

    # добавить продукты
    elif req['request']['nlu']['intents'].get("add_items_nltk"):  # TODO: "add_items"
        tokens = req['request']['nlu']['tokens']
        intent_start = req['request']['nlu']['intents']['add_items_nltk']['slots']['food']['tokens']['start']
        intent_end = req['request']['nlu']['intents']['add_items_nltk']['slots']['food']['tokens']['end']

        gr_i = parser.gramma_info(tokens, intent_start, intent_end)
        products, quantities, units = parser.tokens_parser(gr_i)  # TODO: "units"
        response.add_items_response(res, products, quantities)
        db.add_items(conn, user_id, products, quantities)

    # удалить продукты
    elif req['request']['nlu']['intents'].get("del_items"):
        tokens = req['request']['nlu']['tokens']
        intent_start = int(req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['start'])
        intent_end = int(req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['end'])

        gr_i = parser.gramma_info(tokens, intent_start, intent_end)
        products, quantities, units = parser.tokens_parser(gr_i)  # TODO: "units"
        response.del_items_response(res, products, quantities)
        db.del_items(conn, user_id, products, quantities)

    # обработка кнопок "- перец(1)"
    elif req['request'].get("command") and req['request']['original_utterance'][0:2] == "- ":
        products, quantities, units = [], [], []
        product = ' '.join(req['request']['nlu']['tokens'][0:-1])
        quantity = req['request']['nlu']['tokens'][-1]
        products.append(product)
        quantities.append(quantity)
        # TODO: units.append(req['request']['nlu']['tokens'][2])
        db.del_items(conn, user_id, products, quantities)
        response.del_items_response(res, products, quantities)

    # показать список
    elif req['request']['nlu']['intents'].get("get_items"):
        shopping_list = db.get_items(conn, user_id)
        response.get_items_response(res, shopping_list)

    else:
        res['response']['text'] = 'Кайф!'

    return
