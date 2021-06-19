# coding: utf-8
from __future__ import unicode_literals
from pprint import pformat
from utils import db, response, parser, config, suggest

import json
import logging
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    try:
        user_id = req['session']['user']['user_id']
    except:
        user_id = req['session']['application']['application_id']

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

    ###
    # добавить продукты
    elif req['request']['nlu']['intents'].get("add_items"):
        tokens = req['request']['nlu']['tokens']
        intent_start = req['request']['nlu']['intents']['add_items']['slots']['food']['tokens']['start']
        intent_end = req['request']['nlu']['intents']['add_items']['slots']['food']['tokens']['end']

        tokens_no_stopwords, gr_i = parser.gramma_info(tokens, intent_start, intent_end)
        products, quantities, units, products_orig, units_orig = parser.tokens_parser(tokens_no_stopwords, gr_i)
        response.add_items_response(res, products_orig, quantities, units_orig)
        db.add_items(conn, user_id, products, quantities, units)

    # обработка кнопок "+ <товар>"
    elif req['request'].get("command") and req['request']['original_utterance'][0:2] == "+ ":
        tokens = req['request']['nlu']['tokens']
        product_tokens = [token for token in tokens if len(token) > 1]
        product = ' '.join(product_tokens)
        orig = parser.make_agree(product, by='gr_case', gr_case='accs')
        response.add_items_response(res, [orig], [1], [None])
        db.add_items(conn, user_id, [product], [1], [None])
    ###

    ###
    # удалить продукты
    elif req['request']['nlu']['intents'].get("del_items"):
        tokens = req['request']['nlu']['tokens']
        intent_start = int(req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['start'])
        intent_end = int(req['request']['nlu']['intents']['del_items']['slots']['food']['tokens']['end'])

        tokens_no_stopwords, gr_i = parser.gramma_info(tokens, intent_start, intent_end)
        products, quantities, units, products_orig, units_orig = parser.tokens_parser(tokens_no_stopwords, gr_i)
        response.del_items_response(res, products_orig, quantities, units_orig)
        db.del_items(conn, user_id, products, quantities)
        db.update_freq(conn, user_id, products)

    # обработка кнопок "- <товар>, <кол-во>"
    elif req['request'].get("command") and req['request']['original_utterance'][0:2] == "- ":
        tokens = req['request']['nlu']['tokens']
        product_tokens = [token for token in tokens if len(token) > 1]
        quantity = [token for token in tokens if token.isnumeric()][0]
        product = ' '.join(product_tokens)
        orig = parser.make_agree(product, by='gr_case', gr_case='accs')
        response.del_items_response(res, [orig], [quantity], [None], minus=True)
        db.del_items(conn, user_id, [product], [quantity])
        db.update_freq(conn, user_id, [product])
    ###

    # показать список
    elif req['request']['nlu']['intents'].get("get_items"):
        shopping_list = db.get_items(conn, user_id)
        response.get_items_response(res, shopping_list)

    # обработка периодичных рекомендаций
    elif req['request']['nlu']['intents'].get("get_recs_freq"):
        product_freq_cron = db.get_freq(conn, user_id)
        recs_freq = suggest.suggest_freq(product_freq_cron)
        response.suggest_freq_response(res, recs_freq)

    # вывод стоимости товара
    elif req['request']['nlu']['intents'].get("cost_items"):
        product_quantity = db.get_items(conn, user_id, for_cost=True)
        if len(product_quantity) > 0:
            products = list(zip(*product_quantity))[0]
        else:
            response.get_cost_response(res, [], [])
        product_prices = db.get_cost(conn, products)
        response.get_cost_response(res, product_prices, product_quantity)

    # обработка рецептурных рекомендаций
    elif req['request']['nlu']['intents'].get("suggest_items_recipes"):
        pass

    # удаление таблицы из БД
    elif req['request']['nlu']['intents'].get("reload"):
        db.purge_table(conn)
        res['response']['text'] = 'ТАБЛИЦА УДАЛЕНА'

    else:
        res['response']['text'] = req['request']['original_utterance']

    return 'case'


def db_handler(case):
    if case == 'new_session':
        pass
    elif case == '':
        pass


'''
TEST_PHRASE:
<<<ADD GOLD>>>
Добавь в список покупок 1 бутылку воды, 2 килограмма огурцов, 2 помидора, репчатый лук, острую морковку по-корейски, сметану и упаковку молока, 2 пачки масла и колбасу, пармезан, а ещё, пожалуйста, острую приправу для лосося и пачку чая.
<<<ADD NORM>>>
Добавь в список покупок 1 бутылку воды, огурцы, помидоры, острую морковку по-корейски в кляре, сметану и пакет молока, 2 бутылки оливкового масла и колбасу, пармезан, а ещё острую приправу для сырого лосося и хороший бальзам для лица и нежный чай.
<<<ADD TRASH>>>
Добавь следующие продукты: лосось в сладком соусе, кашу геркулес из ананасов и свежую ножку курицы, ещё бы не помешала рис круглозерный.
<<<ADD TRASH>>>
Удали из списка 3 лосося, кашу, 2 помидора, 10 сметан и пакет молока ещё 3 бутылки воды, воду и колбасу
'''
