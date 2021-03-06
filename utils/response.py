def add_items_response(res, products_orig, quantities, units_orig):
    '''
    Ответ системы пользователю в случае добавления товаров
    '''
    if len(products_orig) == 1:
        res['response']['text'] = (f'Добавила {"" if int(quantities[0]) == 1 else quantities[0]} '
                                   f'{"" if units_orig[0] is None else units_orig[0] + " "}{products_orig[0]} в ваш список покупок.')
    else:
        origs_text = items_to_text(products_orig, quantities, units_orig)
        res['response']['text'] = f'Добавила в ваш список покупок {origs_text}.'

    res['response'].setdefault('buttons', []).append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': True})
    res['response']['buttons'].append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': False})
    return


def del_items_response(res, products_orig: list, quantities: list, units_orig, minus=False):
    '''
    Ответ системы пользователю в случае удаления товаров
    '''
    if minus == True:
        res['response']['text'] = (f'Удалила {"" if units_orig[0] is None else units_orig[0] + " "}'
                                   f'{products_orig[0]} из вашего списка покупок.')

    elif len(products_orig) == 1:
        res['response']['text'] = (f'Удалила {"" if int(quantities[0]) == 1 else quantities[0]} '
                                   f'{"" if units_orig[0] is None else units_orig[0] + " "}{products_orig[0]} из вашего списка покупок.')
    else:
        origs_text = items_to_text(products_orig, quantities, units_orig)
        res['response']['text'] = f'Удалила из вашего списка покупок {origs_text}.'

    res['response'].setdefault('buttons', []).append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': True})
    res['response']['buttons'].append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': False})
    '''
    res['response']['buttons'].append(
        {'title': 'Очистить',
         'payload': 'del_all',
         'hide': True})
    '''
    return


def get_items_response(res, shopping_list):
    '''
    Ответ системы пользователю в случае получения текущего списка покупок
    '''
    if not shopping_list:
        res['response']['text'] = 'Ваш список покупок пока пуст.'
    else:
        res['response']['text'] = 'Список покупок:'
        show_shopping_list(res, shopping_list)
        '''
        res['response'].setdefault('buttons', []).append(
            {'title': 'Очистить',
             'payload': 'del_all',
             'hide': True})
        '''
    return


def show_shopping_list(res, shopping_list):
    '''
    Форматирование текущего списка покупок для ответа пользователю
    '''
    for item in shopping_list:
        res['response'].setdefault('buttons', []).append(
            {'title': f'- {item[0]}, {item[1]} {item[2][0] + "." if item[2] != "-1" else ""}',
             'payload': 'del',
             'hide': False})


def items_to_text(products_orig: list, quantities: list, units_orig):
    '''
    Форматирование списка добавленных/удаленных товаров для ответа пользователю
    '''
    origs_text = ', '.join((f'{"" if quantities[i] == 1 else quantities[i]} '
                            f'{"" if units_orig[i] is None else units_orig[i]} {products_orig[i]}')
                           for i in range(len(products_orig) - 1))
    origs_text = (f'{origs_text} и {"" if quantities[-1] == 1 else quantities[-1]}'
                  f'{"" if units_orig[-1] is None else units_orig[-1]} {products_orig[-1]}')
    return origs_text


def suggest_freq_response(res, recs_freq):
    '''
    Ответ системы пользователю в случае получения рекомендации по периодически покупаемым товарам
    '''
    if len(recs_freq) > 0:
        res['response']['text'] = 'Возможно Вам стоит купить:'

        for item in recs_freq:
            res['response'].setdefault('buttons', []).append(
                {'title': f'+ {item}',
                 'payload': 'del',
                 'hide': False})
    else:
        res['response']['text'] = 'Похоже Вы уже все купили'
    return


def suggest_recipes_response(res, recs_recipes):
    '''
    Ответ системы пользователю в случае получения рекомендации по рецептам
    '''
    if len(recs_recipes) > 0:
        res['response']['text'] = 'Возможно Вы хотели приготовить:'

        for item in recs_recipes:
            res['response'].setdefault('buttons', []).append(
                {'title': f'https://eda.ru{item}',
                 'url': f'https://eda.ru{item}',
                 'payload': 'del',
                 'hide': False})
    else:
        res['response']['text'] = 'Извините, не нашла подходящих рецептов'
    return


def get_cost_response(res, product_prices, product_quantity):
    '''
    Ответ системы пользователю в случае получения стоимости товаров в корзине
    '''
    cost = 0
    product_prices = {product: price for product, price in product_prices}
    for product, quantity in product_quantity:
        cost += quantity * product_prices.get(product, 100)
    res['response']['text'] = f'Стоимость товаров составляет примерно {cost} руб.'
    return
