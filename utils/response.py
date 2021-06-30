from utils.parser import make_agree


def add_items_response(res, products: list):
    '''
    Ответ системы пользователю в случае добавления товаров
    '''
    if len(products) == 0:
        res['response']['text'] = 'Повторите, пожалуйста'
        return

    if len(products) == 1:
        res['response']['text'] = (f'Добавила {products[0]} в ваш список покупок.')
    else:
        origs_text = items_to_text(products)
        res['response']['text'] = f'Добавила в ваш список покупок {origs_text}.'

    # res['response'].setdefault('buttons', []).append(
    #     {'title': 'Список покупок',
    #      'payload': 'get_items',
    #      'hide': True})

    res['response']['buttons'].append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': False})
    return


def del_items_response(res, products: list):
    '''
    Ответ системы пользователю в случае удаления товаров
    '''
    if len(products) == 0:
        res['response']['text'] = 'Ваш список покупок теперь пуст!'
        return

    if len(products) == 1:
        product = make_agree(products[0], by='gr_case', gr_case='accs')
        res['response']['text'] = (f'Удалила {product} из вашего списка покупок.')
    else:
        origs_text = items_to_text(products)
        res['response']['text'] = f'Удалила из вашего списка покупок {origs_text}.'

    res['response']['buttons'].append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': False})
    '''
    res['response'].setdefault('buttons', []).append(
        {'title': 'Список покупок',
         'payload': 'get_items',
         'hide': True})
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
        res['response']['text'] = 'Ваш список покупок:'
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
             'payload': 'del_items',
             'hide': False})


def items_to_text(products: list):
    '''
    Форматирование списка добавленных/удаленных товаров для ответа пользователю
    '''
    products = [make_agree(product, by='gr_case', gr_case='accs') for product in products]
    origs_text = ', '.join(f'{products[i]}' for i in range(len(products) - 1))
    origs_text = f'{origs_text} и {products[-1]}'
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
                 'payload': 'add_items',
                 'hide': False})
    else:
        res['response']['text'] = 'Похоже Вы уже все купили'
    return


def suggest_recipes_response(res, recs_recipes):
    '''
    Ответ системы пользователю в случае получения рекомендации по рецептам
    '''
    if len(recs_recipes) > 0:
        res['response']['text'] = 'Предлагаю Вам следующие рецепты:'

        for item in recs_recipes:
            res['response'].setdefault('buttons', []).append(
                {'title': f'https://eda.ru{item}',
                 'url': f'https://eda.ru{item}',
                 'payload': 'recipes',
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
