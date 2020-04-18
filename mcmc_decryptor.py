import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


class MetropolisDecryptor:
    def __init__(self, alphabet, m, scaling_factor=1.0, broken=False):
        self.alphabet = alphabet
        self.m = m
        self.scaling_factor = scaling_factor
        self.broken = broken
        self.symbols = []
        self.text = ''
        self.log_score = 0
        self.best_score = 0
        self.map = {}
        self.best_map = {}
        self.accept_history = []
        self.score_history = []

    def start_from(self, s, stat=True):
        """Обработать новый текст, инициализировать параметры"""
        sym = set(s)
        if not s:
            # print('Empty text!')
            return False
        if len(sym) > len(self.alphabet):
            # print(f'Too many symbols: {"".join(sym)}')
            return False
        self.text = s
        self.symbols = sorted(list(sym))
        if stat:
            cnt = Counter(s)
            self.symbols.sort(key=cnt.get, reverse=True)
        self.map = {}
        for ind, sym in enumerate(self.symbols):
            self.map[sym] = self.alphabet[ind]
        self.log_score = self.compute_score(self.map)
        self.best_map = self.map.copy()
        self.best_score = self.log_score
        self.accept_history = []
        self.score_history = []
        return True

    def compute_score(self, cur_map):
        """Вычислить score текста, расшифрованоого данной cur_map"""
        m_values = np.zeros(len(self.text) - 1, dtype=np.float64)
        for i in range(len(self.text) - 1):
            pair = ''.join(cur_map[ch] for ch in self.text[i:i + 2])
            m_values[i] = self.m[pair]
        return m_values.sum()

    def metropolis_step(self):
        """Шаг алгоритма"""
        sym1, sym2 = np.random.choice(self.symbols, 2, replace=False)
        new_map = self.map.copy()
        new_map[sym1], new_map[sym2] = new_map[sym2], new_map[sym1]
        old_score = self.log_score
        new_score = self.compute_score(new_map)

        metropolis_condition = np.log(np.random.rand()) < (new_score - old_score) * self.scaling_factor
        if new_score > old_score or (not self.broken and metropolis_condition):
            self.map = new_map
            self.log_score = new_score
            if self.log_score > self.best_score:
                self.best_score = self.log_score
                self.best_map = self.map
            self.accept_history.append(True)
            self.score_history.append(self.log_score)
            return True

        self.accept_history.append(False)
        self.score_history.append(self.log_score)
        return False

    def run(self, num_steps, verbose=False, print_every=100, length=100, early_stop=1000):
        """Сделать несколько шагов"""
        if verbose:
            print('Initial text   : ' + self.decrypt(self.map, length))
        not_improving = 0
        for step_num in range(num_steps):
            old_best = self.best_score
            self.metropolis_step()
            if self.best_score > old_best:
                not_improving = 0
            else:
                not_improving += 1
            if not_improving == early_stop:
                break
            if verbose and (step_num + 1) % print_every == 0:
                print(f'Iteration {step_num + 1:5d}: ' + self.decrypt(self.map, length))
        if verbose:
            print('Best score     : ' + self.decrypt(self.best_map, length))

    def decrypt(self, cur_map, length=None):
        """РАсшифровать текст данной cur_map"""
        return ''.join(cur_map[ch] for ch in self.text[:length])

    def acc_rate(self):
        """Процент шагов, принвших замену"""
        acc = np.array(self.accept_history, dtype=bool)
        return f'{100 * acc.sum() / len(acc):.2f}%'

    def final(self):
        """Расшифровка лучшей полученной map"""
        return self.decrypt(self.best_map)

    def plot(self):
        """График score по итерациям"""
        ax = plt.gca()
        plt.plot(self.score_history)
        ax.set_ylabel('Score')
        ax.set_xlabel('Iteration')
        plt.show()
