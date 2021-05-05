from utils.parser import make_agree
from utils import config


def add_items_response(res, products, quantities):
    products_agreed = [make_agree(product, by='case', gr_case='accs') for product in products]
    products_text = ', '.join(products_agreed)
    res['response']['text'] = f'Добавила {products_text} в ваш список покупок.'
    res['response'].setdefault('buttons', []).append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': True})
    res['response']['buttons'].append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': False})
    res['response']['buttons'].append(
        {'title': 'Очистить',
         'payload': 'del_all',
         'hide': True})
    return


def del_items_response(res, products, quantities):
    if len(products) == 1:
        res['response']['text'] = f'Удалила {make_agree(products[0], by="case", gr_case="accs")} из вашего списка покупок'
    else:
        products_agreed = [make_agree(product, by='case', gr_case='accs') for product in products]
        products_text = ', '.join(products_agreed)
        res['response']['text'] = f'Удалила из вашего списка покупок {products_text}'

    res['response'].setdefault('buttons', []).append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': True})
    res['response']['buttons'].append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': False})
    res['response']['buttons'].append(
        {'title': 'Очистить',
         'payload': 'del_all',
         'hide': True})
    return


def get_items_response(res, shopping_list):
    if not shopping_list:
        res['response']['text'] = 'Ваш список покупок пока пуст.'
    else:
        res['response']['text'] = 'Список покупок:'

        for item in shopping_list:
            res['response'].setdefault('buttons', []).append(
                {'title': f'- {item[0]} ({item[1]})',
                 'payload': 'del',
                 'hide': False})

        res['response'].setdefault('buttons', []).append(
            {'title': 'Очистить',
             'payload': 'del_all',
             'hide': True})
    return
