Шаблоны заданий для первой работы
Автоматическое форматирование при помощи black:

$ black -l 100 caesar.py vigenere.py rsa.py
Автоматическая сортировка импортируемых модулей при помощи isort:

$ isort caesar.py vigenere.py rsa.py
Проверить аннотации типов при помощи mypy:

$ mypy caesar.py vigenere.py rsa.py
Запустить доктесты можно так:

$ python -m doctest caesar.py
$ python -m doctest vigenere.py
$ python -m doctest rsa.py
Запустить юнит-тесты с помощью модуля unittest можно так:

$ python -m unittest discover
Или с помощью модуля pytest:

$ pytest tests/test_caesar.py
$ pytest tests/test_vigenere.py
$ pytest tests/test_rsa.py
Для запуска всех тестов:

$ pytest