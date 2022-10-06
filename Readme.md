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
<pre class="hljs" style="display: block; overflow-x: auto; padding: 0.5em; background-color: rgb(240, 240, 240); color: rgb(68, 68, 68);">MacBook-Air-<span class="hljs-string" style="color: rgb(136, 0, 0);">Egor:</span>API_Lesson_3 odins$ python main.py -link <span class="hljs-string" style="color: rgb(136, 0, 0);">https:</span><span class="hljs-comment" style="color: rgb(136, 136, 136);">//dvmn.org</span>
<span class="hljs-string" style="color: rgb(136, 0, 0);">https:</span><span class="hljs-comment" style="color: rgb(136, 136, 136);">//bit.ly/3yoRce5</span></pre>


Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

pip install -r requirements.txt
Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
