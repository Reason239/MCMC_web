import numpy as np
from collections import Counter
from itertools import product
import pickle
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
from mcmc_decryptor import MetropolisDecryptor
from utils import clean, encrypt


if __name__ == '__main__':
    # ⨒⨓⨔⨕⨖⊣⊢⊥⊤ℕℤℚℝℂ∅⊂⊃⊄⊅⊩⊮⊫⊯⊪⊨⊭∀∃∄⊲⊳⊴⊵⋪⋫⋬⋭≍≭≣≺≻≼≽≾≿∈∋∉∌⊞⊟⊠⊡
    np.random.seed(seed=239)
    alphabet, m = pickle.load(open('models/ru.pkl', 'rb'))
    decryptor = MetropolisDecryptor(alphabet, m, scaling_factor=0.5, broken=False)
    print(alphabet)
    symbol_pool = list('⨒⨓⨔⨕⨖⊣⊢⊥⊤ℕℤℚℝℂ∅⊂⊃⊄⊅⊩⊮⊫⊯⊪⊨⊭∀∃∄⊲⊳⊴⊵⋪⋫⋬⋭≍≭≣≺≻≼≽≾≿∈∋∉∌⊞⊟⊠⊡')
    message = clean(open('test_messages/каренина.txt', 'r', encoding='utf8').read()[:], 'ru')
    print(message)
    print(len(message))
    text = encrypt(message, symbol_pool)
    print(text)
    decryptor.start_from(text, True)
    # decryptor.run(100000, verbose=True, print_every=2000, early_stop=None)
    # print(decryptor.acc_rate())
    # print(decryptor.final())
    # decryptor.plot()

    # print(type(decryptor.m['на']))
