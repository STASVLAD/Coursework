from nltk.corpus import stopwords
from utils import config

UNITS = ['килограмм', 'грамм', 'литр', 'пакет', 'пакетик', 'бутылка', 'упаковка', 'булка', 'пачка']
STOP_WORDS = stopwords.words("russian")
STOP_WORDS.extend(['добавь', 'список', 'продуктов', 'продукты', 'продукт', 'другую',
                   'ещё', 'другая', 'купить'])


def gramma_info(tokens, intent_start, intent_end, remove_stopwords=True):
    gr_i = {}

    for i in range(intent_start, intent_end):
        if tokens[i] not in STOP_WORDS:
            p = config.morph.parse(tokens[i])[0]
            if p.normal_form in UNITS:
                gr_i[p.normal_form] = 'UNITS'
            elif p.normal_form.isnumeric():
                gr_i[p.normal_form] = 'NUM'
            else:
                gr_i[p.normal_form] = str(p.tag.POS)

    return gr_i

# TODO: обработка случая "масло оливковое", "приправа для плова"


def tokens_parser(gr_i):
    adj = ''
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
            adj = item
        if pos == 'NOUN':
            if adj:
                item = make_agree(str(adj + ' ' + item))
            products.append(item)
            adj = ''
            if no_quantity:
                quantities.append(1)
            if no_unit:
                units.append(None)
            no_quantity, no_unit = True, True

    return products, quantities, units


def make_agree(product, by='gender', gr_case='nomn'):
    words = product.split()
    if by == 'gender':
        adj = words[0]
        item = words[1]
        item_gender = str(config.morph.parse(item)[0].tag.gender)
        print(item_gender)
        adj_agreed = config.morph.parse(adj)[0].inflect({item_gender}).word
        product_agreed = adj_agreed + ' ' + item
    if by == 'gr_case':
        product_agreed = []
        for w in words:
            w_agreed = config.morph.parse(w)[0].inflect({gr_case}).word
            product_agreed.append(w_agreed)
        product_agreed = ' '.join(product_agreed)
    return product_agreed
