import pymorphy2
from nltk.corpus import stopwords


def init():
    global morph
    morph = pymorphy2.MorphAnalyzer()

    global STOP_WORDS
    STOP_WORDS = stopwords.words("russian")
    STOP_WORDS = [w for w in STOP_WORDS if not str(morph.parse(w)[0].tag.POS) == 'PREP']
    STOP_WORDS.extend(['добавь', 'список', 'продуктов', 'продукты', 'продукт', 'другую',
                       'ещё', 'другая', 'купить', 'пачка'])

    global UNITS
    UNITS = ['килограмм', 'грамм', 'литр', 'пакет', 'пакетик', 'бутылка', 'упаковка', 'булка', 'пачка']
