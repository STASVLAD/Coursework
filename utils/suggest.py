from datetime import datetime
from statistics import median


def suggest_freq(pfc):
    recs = []
    freq_lists = list(zip(*pfc))[1]

    for freq_list in freq_lists:
        for freq in freq-list:
            freq = int(freq[0])

    freq_medians = []
    for freq_list in freq_lists:
        freq_medians.append(median(freq_list))

    for i in range(len(pfc)):
        cron = datetime.strptime(pfc[i][2], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - cron).days - freq_medians[i] >= 0:
            recs.append(pfc[i][0])

    return recs
