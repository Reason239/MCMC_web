import numpy as np
from collections import Counter
from itertools import product
from utils import is_eng, is_rus, clean
import pickle


def train_m(corpus, language='ru'):
    if language.lower() in ['ru', 'rus', 'russian']:
        is_letter = is_rus
    else:
        is_letter = is_eng
    cnt_1 = Counter()
    cnt_2 = Counter()
    with open(corpus, 'r', encoding='utf8') as file:
        for line in file:
            line = clean(line, language)
            if line:
                for i in range(len(line) - 1):
                    if is_letter(line[i]):
                        cnt_1[line[i]] += 1
                        if is_letter(line[i + 1]):
                            cnt_2[line[i:i + 2]] += 1
                if is_letter(line[-1]):
                    cnt_1[line[-1]] += 1
    alphabet = [item[0] for item in cnt_1.most_common()]
    m = {}
    for ch1, ch2 in product(alphabet, repeat=2):
        m[ch1 + ch2] = np.log(cnt_2[ch1 + ch2] + 1)
    return alphabet, m

if __name__ == '__main__':
    pickle.dump(train_m('corpuses/warpeace.txt', 'en'), open('models/en.pkl', 'wb'))
    pickle.dump(train_m('corpuses/война_и_мир.txt', 'ru'), open('models/ru.pkl', 'wb'))