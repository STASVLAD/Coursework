import pymorphy2
import pandas as pd
from nltk.corpus import stopwords


def init():
    global morph
    morph = pymorphy2.MorphAnalyzer()

    global STOP_WORDS
    STOP_WORDS = stopwords.words("russian")
    STOP_WORDS = [w for w in STOP_WORDS if not str(morph.parse(w)[0].tag.POS) == 'PREP']
    except_words = ['все', 'всю', 'всего', 'всех', 'совсем']
    for w in except_words:
        STOP_WORDS.remove(w)
    STOP_WORDS.extend(['добавь', 'список', 'продуктов', 'продукты', 'продукт', 'другую',
                       'ещё', 'другая', 'купить', 'пачка'])

    global UNITS
    UNITS = ['кг', 'г', 'литр', 'пакет', 'пакетик', 'бутылка', 'упаковка', 'булка', 'пачка', 'банка']

    global df
    df = pd.read_json('data/recipes.json')
