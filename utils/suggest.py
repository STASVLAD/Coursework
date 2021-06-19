from datetime import datetime, timedelta
from statistics import median
import numpy as np


def suggest_freq(pfc):
    '''
    рекомендации для периодически покупаемых товаров
    '''
    recs = []

    freq_medians = {}
    for i in range(len(pfc)):
        freqs = np.array(pfc[i][1])
        freqs = freqs[freqs > timedelta(0)]
        if len(freqs) > 0:
            freq_medians[pfc[i][0]] = median(freqs)
        else:
            freq_medians[pfc[i][0]] = timedelta(0)

    for product, freq, cron in pfc:
        # debug: datetime.now() : test = datetime.now() + timedelta(days=2)
        if ((datetime.now() - cron).days >= freq_medians[product].days) and freq_medians[product].days != 0:
            recs.append(product)

    return recs
