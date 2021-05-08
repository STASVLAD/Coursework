from utils import config


def gramma_info(tokens, intent_start, intent_end, remove_stopwords=True):
    gr_i = {}
    # TODO: хранение в словаре повторений
    for i in range(intent_start, intent_end):
        if tokens[i] not in config.STOP_WORDS:
            p = config.morph.parse(tokens[i])[0]
            if p.normal_form in config.UNITS:
                gr_i[p.word] = [p.normal_form, 'UNITS']
            elif p.normal_form.isnumeric():
                gr_i[p.word] = [p.normal_form, 'NUM']
            else:
                gr_i[p.word] = [p.normal_form, str(p.tag.POS)]

    return gr_i

# TODO: обработка случая "масло оливковое", "приправа для плова"


def tokens_parser(gr_i):
    adj, prep = '', ''
    origs, products, quantities, units = [], [], [], []
    no_quantity, no_unit = True, True

    for w_orig, [w_norm, w_pos] in gr_i.items():
        if w_pos == 'NUM':
            quantities.append(int(w_norm))
            no_quantity = False
        if w_pos == 'UNITS':
            units.append(w_norm)
            no_unit = False
        if w_pos == 'ADJF':
            adj = w_norm
            adj_orig = w_orig
        if w_pos == 'PREP':
            prep = w_norm
            prep_orig = w_orig
        if w_pos == 'NOUN':
            if adj:
                w_norm = make_agree(str(adj + ' ' + w_norm))
                w_orig = adj_orig + ' ' + w_orig
            if prep:
                products[-1] = products[-1] + ' ' + prep + ' ' + w_orig
                origs[-1] = origs[-1] + ' ' + prep_orig + ' ' + w_orig
                no_quantity, no_unit = True, True
                adj, prep = '', ''
                continue
            origs.append(w_orig)
            products.append(w_norm)
            if no_quantity:
                quantities.append(1)
            if no_unit:
                units.append(None)
            no_quantity, no_unit = True, True
            adj, prep = '', ''

    return products, quantities, units, origs


def make_agree(product: str, by='gender', gr_case='nomn'):
    words = product.split()
    if by == 'gender':
        adj = words[0]
        item = words[1]
        item_gender = str(config.morph.parse(item)[0].tag.gender)
        adj_agreed = config.morph.parse(adj)[0].inflect({item_gender}).word
        product_agreed = adj_agreed + ' ' + item
    if by == 'gr_case':
        product_agreed = []
        for w in words:
            w_agreed = config.morph.parse(w)[0].inflect({gr_case}).word
            product_agreed.append(w_agreed)
        product_agreed = ' '.join(product_agreed)
    return product_agreed
