def add_items_response(res, origs, quantities):
    if len(origs) == 1:
        res['response']['text'] = f'Добавила {origs[0]} в ваш список покупок.'
    else:
        origs_text = ', '.join(origs[:-1])
        origs_text = origs_text + ' и ' + origs[-1]
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


def del_items_response(res, origs: list, quantities: list):
    if len(origs) == 1:
        res['response']['text'] = f'Удалила {origs[0]} из вашего списка покупок.'
    else:
        origs_text = ', '.join(origs[:-1])
        origs_text = origs_text + ' и ' + origs[-1]
        res['response']['text'] = f'Удалила из вашего списка покупок {origs_text}.'

    # show_shopping_list(res, shopping_list)

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
        show_shopping_list(res, shopping_list)
        res['response'].setdefault('buttons', []).append(
            {'title': 'Очистить',
             'payload': 'del_all',
             'hide': True})
    return


def show_shopping_list(res, shopping_list):
    for item in shopping_list:
        res['response'].setdefault('buttons', []).append(
            {'title': f'- {item[0]} ({item[1]})',
             'payload': 'del',
             'hide': False})
