# coding: utf-8
from __future__ import unicode_literals
from utils import utils
import psycopg2

import json
import logging

from flask import Flask, request
app = Flask(__name__)

# testing
shopping_list = ['молоко', 'сыр', 'хлеб']
# testing

logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    conn = utils.connect()

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response, conn)

    logging.info('Response: %r', response)
    conn.close()

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res, conn):
    user_id = req['user']['user_id']

    if req['session']['new']:
        shopping_list = utils.get_items(conn)

        if not shopping_list:
            res['response']['text'] = 'Привет! Помочь с покупками?'
        else:
            response_text = 'Привет! Твой список покупок:'
            # response_text += TODO: оформить как список картинок
            res['response']['text'] = response_text
            # res['response']['text'] = 'Привет! Не забудь купить {}'.format(shopping_list)

        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)
