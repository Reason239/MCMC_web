from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from mcmc_decryptor import MetropolisDecryptor
from utils import clean, encrypt
import pickle

app = Flask(__name__, static_folder='static')

alphabet_ru, m_ru = pickle.load(open('models/ru.pkl', 'rb'))
decryptor_ru = MetropolisDecryptor(alphabet_ru, m_ru, scaling_factor=1.0, broken=False)
alphabet_en, m_en = pickle.load(open('models/en.pkl', 'rb'))
decryptor_en = MetropolisDecryptor(alphabet_en, m_en, scaling_factor=1.0, broken=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mode = request.form['mode']
        lang = request.form['lang']
        inp = request.form['input_text']
        if mode == 'decipher':
            if lang == 'ru':
                decryptor = decryptor_ru
            else:
                decryptor = decryptor_en

            if not decryptor.start_from(inp):
                return render_template('main.html', result='Некорректный ввод')
            try:
                num_steps = int(request.form['iter'])
            except ValueError:
                return render_template('main.html', result='Некорректный ввод')
            decryptor.run(num_steps)
            result = decryptor.final()
            return render_template('main.html', result=result)
        else:
            result = encrypt(clean(inp, lang))
            return render_template('main.html', result=result)

    return render_template('main.html', result='')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test')
def test():
    message = open('test_messages/encrypted.txt', 'r').read()
    decryptor_ru.start_from(message)
    decryptor_ru.run(5000)
    result = decryptor_ru.final()
    return render_template('main.html', result=result)


if __name__ == '__main__':
    app.run()
# ?
