Основная задача - расшифровка шифров подстановки. О методе можно почитать [тут](http://utstat.toronto.edu/WSFiles/technicalreports/1005.pdf)

Файлы прикладываю. За что отвечает каждый:

#### utils.py

Вспомогательные функции. Понимаем, является ли символ русской или английской буквой, чистим текст от пунктуации, зашифровываем текст.

#### training_models.py

Чтобы алгоритм работал, он должен знать, насколько часто встречается в языке каждая пара последовательных букв. `train_m(corpus, language='ru')` по данному имени файла с большим текстом и языку выдаёт `alphabet` - буквы в порядке от более частым к менее частым и словарь `m`, который по паре букв (строке длины 2) говорит, сколько раз эти две буквы встречались подряд в тексте. 

Если запустить training_models.py, то программа сделает это для русского и английского текстов из папки `corpuses` и сохранит результат в папку `models`.

#### mcmc_decryptor.py

Файл с основным классом `MetropolisDecryptor`. Конструктор принимает `alphabet` и `m`. Умеет кушать текст (метод start_from), очищенный от пунктуации, и инициализировать все параметры. Изначально символы текста ставятся в соответствие (`map`) буквам так, чтобы более частые символы в тексте соответствовали более частым буквам языка.

Каждая попытка расшифровать текст получает score: перемножаем значения m[ch1 + ch2] по всем соседним символам ch1 и ch2 в расшифрованном тексте. (например, 'to the did' получит высокий score, а 'qw qhj xkx' - низкий, потому что такие сочетания букв редки). Метод compute_score вычисляет score текста, расшифрованного данной map. Вспомогательный метод decrypt расшифровывает текст с помощью данной map.

Метод metropolis_step делает шаг алгоритма. Случайно выбираются два символа, и соответствующий им буквы меняются местами. Вычисляется score текста, расшифрованного новым соответствием символ-буква. Если он больше старого, то замена принимается. Если меньше, то принимается с вероятностью (новый score) / (старый score). (на scaling_factor не обращайте внимания, он не пригодился) (опция broken=True заставила бы нас принимать замену только если она увеличивает score. Оказывается, с broken=True на коротких сообщениях работает хуже, так что наворот с принятием замены, уменьшающей score, полезен)

Метод run просто делает много шагов. Может выводить информацию в процессе. Если максимальный score не менялся early_stop итераций, то процесс обрывается.

Метод final переводит текст с помощью map, дающей максимальный score (она в процессе запоминается в best_map)

Метод plot рисует, как в процессе менялся score.

Метод acc_rate выдает, сколько процентов предложенных замен алгоритм принял.

#### testing.py

Тут я тестировал этот класс. Сообщения для тестирования положил в папку test_messages.

#### app.py

Основной файл с приложением. Здесь уже ничего хитрого не происходит. 

Статика лежит в папке static.

Шаблоны - в templates. Есть базовый base.html и наследуемые от него main.html и about.html.

Примеры работы с сайтом смотрите в папке "пример работы".

Для тестирования производительности создана дополнительная страница /test, которая запускает расшифровку фиксированного текста на русском.
