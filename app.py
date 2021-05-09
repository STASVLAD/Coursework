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

    case = dialog_handler(request.json, response, conn)
    db_handler(case)  # TODO: @after_response()

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
            # TODO Описание навыка
            res['response']['text'] = 'Описание навыка'
        else:
            shopping_list = db.get_items(conn, user_id)
            response.get_items_response(res, shopping_list)
            res['response']['text'] = 'Привет!\n' + res['response']['text']

    # очистить список
    elif (req.get('buttons', {}).get('payload') == 'del_all' or
          req['request']['nlu']['intents'].get('del_all_items')):
        res['response']['text'] = 'Ваш список покупок теперь пуст!'
        db.del_items(conn, user_id, all=True)

    # добавить продукты
    elif req['request']['nlu']['intents'].get("add_items"):
        tokens = req['request']['nlu']['tokens']
        intent_start = req['request']['nlu']['intents']['add_items']['slots']['food']['tokens']['start']
        intent_end = req['request']['nlu']['intents']['add_items']['slots']['food']['tokens']['end']

        tokens_no_stopwords, gr_i = parser.gramma_info(tokens, intent_start, intent_end)
        # TODO: "units"
        products, quantities, units, origs = parser.tokens_parser(tokens_no_stopwords, gr_i)
        response.add_items_response(res, origs, quantities)
        db.add_items(conn, user_id, products, quantities)

    # удалить продукты
    elif req['request']['nlu']['intents'].get("del_items"):
        tokens = req['request']['nlu']['tokens']
        intent_start = int(req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['start'])
        intent_end = int(req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['end'])

        tokens_no_stopwords, gr_i = parser.gramma_info(tokens, intent_start, intent_end)
        # TODO: "units"
        products, quantities, units, origs = parser.tokens_parser(tokens_no_stopwords, gr_i)
        response.del_items_response(res, origs, quantities)
        db.del_items(conn, user_id, products, quantities)

    # обработка кнопок "- товар, <кол-во>"
    elif req['request'].get("command") and req['request']['original_utterance'][0:2] == "- ":
        product = ' '.join(req['request']['nlu']['tokens'][0:-1])
        quantity = req['request']['nlu']['tokens'][-1]
        orig = parser.make_agree(product, by='gr_case', gr_case='accs')
        response.del_items_response(res, [orig], [quantity], minus=True)
        db.del_items(conn, user_id, [product], [quantity])

    # показать список
    elif req['request']['nlu']['intents'].get("get_items"):
        shopping_list = db.get_items(conn, user_id)
        response.get_items_response(res, shopping_list)

    # обработка периодичных рекомендаций
    elif req['request']['nlu']['intents'].get("suggest_items_periodic"):
        pass

    # вывод стоимости товара
    elif req['request']['nlu']['intents'].get("cost_items"):
        pass

    # обработка рецептурных рекомендаций
    elif req['request']['nlu']['intents'].get("suggest_items_recipes"):
        pass

    else:
        res['response']['text'] = req['request']['original_utterance']

    return 'case'


def db_handler(case):
    if case == 'new_session':
        pass
    elif case == '':
        pass

#  thread = Thread(target=do_work, kwargs={'value': request.args.get('value', 20)})
#    thread.start()


'''
TEST_PHRASE:
<<<ADD NORM>>>
Добавь в список покупок 1 бутылку воды, огурцы, помидоры, острую морковку по-корейски в кляре, сметану и пакет молока, 2 бутылки оливкового масла и колбасу, пармезан, а ещё острую приправу для сырого лосося и хороший бальзам для лица и нежный чай.
<<<ADD TRASH>>>
Добавь следующие продукты: лосось в сладком соусе, кашу геркулес из ананасов и свежую ножку курицы, ещё бы не помешала рис круглозерный.
<<<ADD TRASH>>>
Удали из списка 3 лосося, кашу, 2 помидора, 10 сметан и пакет молока ещё 3 бутылки воды, воду и колбасу
'''
