import pymorphy2
from nltk.corpus import stopwords

UNITS = ['килограмм', 'грамм', 'литр', 'пакет', 'пакетик', 'бутылка', 'упаковка', 'булка', 'пачка']
# 'буханка',

stop_words = stopwords.words("russian")
stop_words.extend(['добавь', 'список', 'продуктов', 'продукты', 'продукт', 'другую', 'ещё', 'другая', 'купить'])

tokens = ["добавь", "в", "список", "покупок", "плиз", "1", "пачку", "перца", "2", "бутылки", "оливкого", "масла", "и",
          "3", "пакетика", "петрушки", "а", "ещё", "и", "килограмм", "картошку", "потом", "надо", "купить", "ещё", "литр", "сока"]


def gramma_info(tokens, morph, intent_start, intent_end, remove_stopwords=True):
    gramma_info = {}

    for i in range(intent_start, intent_end):
        if tokens[i] not in stop_words:
            p = morph.parse(tokens[i])[0]
            if p.normal_form in UNITS:
                gramma_info[p.normal_form] = 'UNITS'
            elif p.normal_form.isnumeric():
                gramma_info[p.normal_form] = 'NUM'
            else:
                gramma_info[p.normal_form] = str(p.tag.POS)

    return gramma_info


gr_i = gramma_info(tokens, pymorphy2.MorphAnalyzer(), 5, 27, remove_stopwords=True)

product = ''
products = []
quantities = []
units = []
no_quantity, no_unit, no_adj = True, True, True

for item, pos in gr_i.items():
    if pos == 'NUM':
        quantities.append(int(item))
        no_quantity = False
    if pos == 'UNITS':
        units.append(item)
        no_unit = False
    if pos == 'ADJF':
        product = item + ' '
        no_adj = False
    if pos == 'NOUN':
        product += item
        products.append(product)
        product = ''
        if no_quantity:
            quantities.append(1)
        if no_unit:
            units.append(None)
        no_quantity, no_unit, no_adj = True, True, True
