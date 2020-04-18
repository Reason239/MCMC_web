import numpy as np
import re


# ENG: from 97 to 122
def is_eng(char):
    return 97 <= ord(char) <= 122 or char == ' '


# RUS: from 1072 to 1103 and 1104
def is_rus(char):
    return 1072 <= ord(char) <= 1103 or char == ' ' or ord(char) == 1105


def clean(s, language='ru'):
    if language.lower() in ['ru', 'rus', 'russian']:
        is_letter = is_rus
    else:
        is_letter = is_eng
    s2 = ''.join(ch if ch != '\n' else ' ' for ch in s.lower() if is_letter(ch) or ch == ' ' or ch == '\n')
    return re.sub(' +', ' ', s2)


def encrypt(text, symbol_pool=None):
    if not symbol_pool:
        symbol_pool = list('⨒⨓⨔⨕⨖⊣⊢⊥⊤ℕℤℚℝℂ∅⊂⊃⊄⊅⊩⊮⊫⊯⊪⊨⊭∀∃∄⊲⊳⊴⊵⋪⋫⋬⋭≍≭≣≺≻≼≽≾≿∈∋∉∌⊞⊟⊠⊡')
    text_chars = sorted(list(set(text)))
    new_chars = np.random.choice(symbol_pool, len(text_chars), replace=False)
    replace_map = dict(zip(text_chars, new_chars))
    return ''.join(replace_map[ch] for ch in text)


def get_message(name, length=None):
    if is_rus(name[0]):
        lang = 'ru'
    else:
        lang = 'en'
    text = open('test_messages/' + name + '.txt', 'r', encoding='utf8').read()
    initial = clean(text, lang).strip()[:length]
    encrypted = encrypt(initial)
    return initial, encrypted
