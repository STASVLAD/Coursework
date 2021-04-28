# coding: utf-8
from __future__ import unicode_literals
import psycopg2

import json
import logging

from flask import Flask, request
app = Flask(__name__)

# testing
shopping_list = ['молоко', 'сыр', 'хлеб']
# testing

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.


@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.


def handle_dialog(req, res):
    user_id = req['user']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'shopping_list': shopping_list
        }

        if not shopping_list:
            res['response']['text'] = 'Привет! Помочь с покупками?'
        else:
            res['response']['text'] = 'Привет! Не забудь купить {}'.format(shopping_list)

        res['response']['buttons'] = get_suggests(user_id)
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

# Функция возвращает две подсказки для ответа.


def get_suggests(user_id):
    session = sessionStorage[user_id]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    with conn.cursor() as cursor:
        conn.autocommit = True
        values = [
            ('ALA', 'Almaty', 'Kazakhstan'),
            ('TSE', 'Astana', 'Kazakhstan'),
            ('PDX', 'Portland', 'USA'),
        ]
        insert = sql.SQL('INSERT INTO city (code, name, country_name) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        cursor.execute(insert)

    return suggests
