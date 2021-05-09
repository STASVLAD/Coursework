def add_items_response(res, origs, quantities):
    if len(origs) == 1:
        res['response']['text'] = (f'Добавила {"" if int(quantities[0]) == 1 else quantities[0]} '
                                   f'{origs[0]} в ваш список покупок.')
    else:
        origs_text = items_to_text(origs, quantities)
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


def del_items_response(res, origs: list, quantities: list, minus=False):
    if minus == True:
        res['response']['text'] = f'Удалила {origs[0]} из вашего списка покупок.'

    elif len(origs) == 1:
        res['response']['text'] = (f'Удалила {"" if int(quantities[0]) == 1 else quantities[0]} '
                                   f'{origs[0]} из вашего списка покупок.')
    else:
        origs_text = items_to_text(origs, quantities)
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
    '''
    res['response']['buttons'].append(
        {'title': 'Очистить',
         'payload': 'del_all',
         'hide': True})
    '''
    return


def get_items_response(res, shopping_list):
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
    for item in shopping_list:
        res['response'].setdefault('buttons', []).append(
            {'title': f'- {item[0]}, {item[1]}',
             'payload': 'del',
             'hide': False})


def items_to_text(origs: list, quantities: list):
    origs_text = ', '.join(f'{"" if quantities[i] == 1 else quantities[i]} {origs[i]}'
                           for i in range(len(origs) - 1))
    origs_text = f'{origs_text} и {"" if quantities[-1] == 1 else quantities[-1]} {origs[-1]}'
    return origs_text
