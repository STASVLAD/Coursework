from utils import db


def session_new_response(res, conn, user_id):
    if not db.is_new_user(conn, user_id):
        res['response']['text'] = 'Описание навыка'  # TODO Описание навыка
    else:
        shopping_list = db.get_items(conn, user_id)
        if not shopping_list:
            res['response']['text'] = 'Привет! Твой список покупок пуст :(\nПомочь с покупками?'
        else:
            res['response']['text'] = 'Привет!'
            res['response'].setdefault('card', {})['type'] = "BigImage"
            res['response']['card'][''] = 'Привет! Твой список покупок:'
            res['response']['card'].setdefault('items', []).append({"title": "Молоко"})
            res['response']['card']['items'][0]['description'] = 'description0\ndescription0\ndescription0'
            res['response']['card']['items'].append({"title": "Заголовок для изображения 1"})
            res['response']['card']['items'][1]['description'] = 'description1\ndescription1\ndescription1'
            res['response']['card']['items'].append({"title": "Заголовок для изображения 1"})
            res['response']['card']['items'][2]['description'] = 'description1\ndescription1\ndescription1'
            res['response']['card']['items'].append({"title": "Заголовок для изображения 1"})
            res['response']['card']['items'][3]['description'] = 'description1\ndescription1\ndescription1'
            res['response']['card']['items'].append({"title": "Заголовок для изображения 1\n\n\n\n"})
            res['response']['card']['items'][4]['description'] = 'description1\ndescription1\ndescription1\n\n\n\n'
            res['response'].setdefault('buttons', []).append({'title': 'Очистить'})
            res['response']['buttons'][0]['payload'] = 'del_all'
            res['response']['buttons'][0]['hide'] = True

    return


def add_items_response(res, conn, user_id, products, quantities):
    res['response'].setdefault('card', {})['type'] = "ItemsList"
    res['response']['card'].setdefault('header', {})['text'] = 'Привет! Твой список покупок:'
    res['response']['card'].setdefault('items', []).append({"title": "Заголовок для изображения 0"})
    res['response']['card']['items'][0]['description'] = 'description0\ndescription0\ndescription0'
    res['response']['card']['items'].append({"title": "Заголовок для изображения 1"})
    res['response']['card']['items'][1]['description'] = 'description1\ndescription1\ndescription1'
    res['response'].setdefault('buttons', {})['title'] = 'Очистить'
    res['response']['buttons']['payload'] = 'del_all'
    res['response']['buttons']['hide'] = True

    return
