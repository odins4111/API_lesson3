Проект позволяет создавать короткие ссылки с помошью API сервиса Bitly.

Уникальный

Для работы сервиса нужен уникальный токен BitLy, который можно получить на официальном сайте. Токен внутри проекта берётся из переменных окружения. Чтобы их определить, создайте файл .env и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=токен.


Описание работы:

Скрипт может работать в двух режимах:
1. Создавать короткие ссылки
2. Получать информацию о переходах по коротким ссылкам.

Создание короткой ссылки

Необходимо запусть скрипт с параметром -link и передать ссылку в формате https://example.ru
Результатом работы будет короткая ссылка, которую сгенирирует сервис
<p class="has-line-data" data-line-start="0" data-line-end="2">MacBook-Air-Egor:API_Lesson_3 odins$ python <a href="http://main.py">main.py</a> -link <a href="https://dvmn.org">https://dvmn.org</a><br>
<a href="https://bit.ly/3yoRce5">https://bit.ly/3yoRce5</a></p>


Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

pip install -r requirements.txt
Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
