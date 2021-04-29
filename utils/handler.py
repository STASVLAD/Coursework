from utils import utils


def session_new_handler(res, conn, user_id):
    if utils.is_new_user(user_id):
        res['response']['text'] = 'Описание навыка'  # TODO Описание навыка
    else:
        shopping_list = utils.get_items(conn, user_id)
        if not shopping_list:
            res['response']['text'] = 'Привет! Твой список покупок пуст :(.\nПомочь с покупками?'
        else:
            res['response']['card']['type'] = "ItemsList"
            res['response']['card']['header'] = 'Привет! Твой список покупок:'
            res['response']['card']['items'][0]["title"] = "Заголовок для изображения 0"
            res['response']['card']['items'][0]['description'] = 'description0\ndescription0\ndescription0'
            res['response']['card']['items'][1]["title"] = "Заголовок для изображения 1"
            res['response']['card']['items'][1]['description'] = 'description1\ndescription1\ndescription1'
            res['response']['buttons']['title'] = 'Очистить'
            res['response']['buttons']['payload'] = 'del_all'
            res['response']['buttons']['hide'] = True

    return
