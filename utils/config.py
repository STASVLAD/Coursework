import pymorphy2


def init():
    global morph
    morph = pymorphy2.MorphAnalyzer()
