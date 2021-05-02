from nltk.corpus import stopwords

UNITS = ['килограмм', 'грамм', 'литр', 'пакет', 'пакетик', 'бутылка', 'упаковка', 'булка', 'пачка']
STOP_WORDS = stopwords.words("russian")
STOP_WORDS.extend(['добавь', 'список', 'продуктов', 'продукты', 'продукт', 'другую',
                   'ещё', 'другая', 'купить'])


def gramma_info(morph, tokens, intent_start, intent_end, remove_stopwords=True):
    gr_i = {}

    for i in range(intent_start, intent_end):
        if tokens[i] not in STOP_WORDS:
            p = morph.parse(tokens[i])[0]
            if p.normal_form in UNITS:
                gr_i[p.normal_form] = 'UNITS'
            elif p.normal_form.isnumeric():
                gr_i[p.normal_form] = 'NUM'
            else:
                gr_i[p.normal_form] = str(p.tag.POS)

    return gr_i


def tokens_parser(gr_i):
    product = ''
    products = []
    quantities = []
    units = []
    no_quantity, no_unit = True, True

    for item, pos in gr_i.items():
        if pos == 'NUM':
            quantities.append(int(item))
            no_quantity = False
        if pos == 'UNITS':
            units.append(item)
            no_unit = False
        if pos == 'ADJF':
            product = item + ' '
        if pos == 'NOUN':
            product += item
            products.append(product)
            product = ''
            if no_quantity:
                quantities.append(1)
            if no_unit:
                units.append(None)
            no_quantity, no_unit = True, True

    return products, quantities, units
