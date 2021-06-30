from utils import config


def gramma_info(tokens, intent_start, intent_end):
    '''
    Удаление стоп-слов, лемматизация, определение POS-тэгов (число/единица измерения/часть речи)
    '''
    gr_i = {}
    tokens_no_stopwords = []

    for i in range(intent_start, intent_end):
        try:
            if tokens[i] not in config.STOP_WORDS:
                tokens_no_stopwords.append(tokens[i])
                p = config.morph.parse(tokens[i])[0]
                if p.normal_form in config.UNITS:
                    gr_i.setdefault(tokens[i], {})['normal_form'] = p.normal_form
                    gr_i[tokens[i]]['pos'] = 'UNITS'
                elif (p.normal_form.isnumeric() or p.normal_form == 'всё' or
                      p.normal_form == 'все' or p.normal_form == 'весь'):
                    gr_i.setdefault(tokens[i], {})['normal_form'] = p.normal_form
                    gr_i[tokens[i]]['pos'] = 'NUM'
                else:
                    gr_i.setdefault(tokens[i], {})['normal_form'] = p.normal_form
                    gr_i[tokens[i]]['pos'] = str(p.tag.POS)
        except IndexError:
            continue

    return tokens_no_stopwords, gr_i


def tokens_parser(tokens_no_stopwords, gr_i):
    '''
    Парсер запросов
    '''
    adj, prep = '', ''
    products_orig, products, quantities, units_orig, units = [], [], [], [], []
    no_quantity, no_unit = True, True

    for token in tokens_no_stopwords:
        if gr_i[token]['pos'] == 'NUM':
            try:
                quantities.append(int(gr_i[token]['normal_form']))
            except ValueError:
                quantities.append(gr_i[token]['normal_form'])
            no_quantity = False
        if gr_i[token]['pos'] == 'UNITS':
            units.append(gr_i[token]['normal_form'])
            units_orig.append(token)
            no_unit = False
        if gr_i[token]['pos'] == 'ADVB':
            if prep:
                try:
                    products[-1] = products[-1] + ' ' + prep + ' ' + token
                    products_orig[-1] = products_orig[-1] + ' ' + prep_orig + ' ' + token
                except IndexError:
                    pass
                prep = ''
            else:
                try:
                    products[-1] = products[-1] + ' ' + token
                    products_orig[-1] = products_orig[-1] + ' ' + token
                except IndexError:
                    pass
        if gr_i[token]['pos'] == 'ADJF':
            adj = gr_i[token]['normal_form']
            adj_orig = token
        if gr_i[token]['pos'] == 'PREP':
            prep = gr_i[token]['normal_form']
            prep_orig = token
        if gr_i[token]['pos'] == 'NOUN':
            w_orig = token
            w_norm = gr_i[token]['normal_form']
            if adj:
                w_norm = make_agree(str(adj + ' ' + w_norm))
                w_orig = adj_orig + ' ' + w_orig
            if prep:
                try:
                    products[-1] = products[-1] + ' ' + prep + ' ' + w_orig
                    products_orig[-1] = products_orig[-1] + ' ' + prep_orig + ' ' + w_orig
                except IndexError:
                    pass
                no_quantity, no_unit = True, True
                adj, prep = '', ''
                continue
            products_orig.append(w_orig)
            products.append(w_norm)
            if no_quantity:
                quantities.append(1)
            if no_unit:
                units.append(None)
                units_orig.append(None)
            no_quantity, no_unit = True, True
            adj, prep = '', ''

    return products, quantities, units, products_orig, units_orig


def make_agree(product: str, by='gender', gr_case='nomn'):
    '''
    Согласование слов по роду и падежу
    '''
    words = product.split()
    if by == 'gender':
        adj = words[0]
        item = words[1]
        item_gender = str(config.morph.parse(item)[0].tag.gender)
        try:
            adj_agreed = config.morph.parse(adj)[0].inflect({item_gender}).word
        except:
            adj_agreed = adj
        words = adj_agreed + ' ' + item
    if by == 'gr_case':
        for i in range(len(words)):
            try:
                words[i] = config.morph.parse(words[i])[0].inflect({gr_case}).word
            except:
                break
        words = ' '.join(words)
    return words


def remove_duplicates(products, quantities, units):
    no_dupes = ([], [], [])
    for i in range(len(products)):
        if products[i] not in no_dupes[0]:
            no_dupes[0].append(products[i])
            no_dupes[1].append(quantities[i])
            no_dupes[2].append(units[i])
        else:
            j = no_dupes[0].index(products[i])
            no_dupes[1][j] += quantities[i]
    return no_dupes
