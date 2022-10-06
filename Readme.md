Проект позволяет создавать короткие ссылки с помошью API сервиса Bitly.

<h1>Подготовка к работе</h1>

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

<pre class="hljs" style="display: block; overflow-x: auto; padding: 0.5em; background-color: rgb(240, 240, 240); color: rgb(68, 68, 68);">pip install -<span class="hljs-keyword" style="font-weight: 700;">r</span> requirements.txt</pre>

Для работы сервиса нужен уникальный токен BitLy, который можно получить на <a href="https://dev.bitly.com>">официальном сайте</a>. Токен внутри проекта тянется из переменных окружения. Чтобы их установить, создайте внутри репозитория файл .env и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=токен.

Пример файла .env:
<pre class="hljs" style="display: block; overflow-x: auto; padding: 0.5em; background-color: rgb(240, 240, 240); color: rgb(68, 68, 68);"><span class="hljs-attr">BITLY_TOKEN</span>=<span class="hljs-number" style="color: rgb(136, 0, 0);">34</span>dsgfdg34324sdfsdf0sdff234432</pre>




<h1>Описание работы</h1>

Скрипт может работать в двух режимах:
1. Создавать короткие ссылки
2. Получать информацию о переходах по коротким ссылкам.

<h3>Создание короткой ссылки</h3>

Необходимо запусть скрипт с параметром -link и передать ссылку в формате https://example.ru.
Результатом работы будет короткая ссылка, которую сгенирирует сервис.

Пример:
<pre class="hljs" style="display: block; overflow-x: auto; padding: 0.5em; background-color: rgb(240, 240, 240); color: rgb(68, 68, 68);">python main.py -link <span class="hljs-string" style="color: rgb(136, 0, 0);">https:</span><span class="hljs-comment" style="color: rgb(136, 136, 136);">//dvmn.org</span>
<span class="hljs-string" style="color: rgb(136, 0, 0);">https:</span><span class="hljs-comment" style="color: rgb(136, 136, 136);">//bit.ly/3yoRce5</span>
</pre>

<h3>Получение информаии о переходах по ссылкам</h3>

Необходимо запусть скрипт с параметром -link и передать коротку ссылку в формате https://bit.ly/XXXXXX.
Результатом работы будет сумма кликов по определнной короткой ссылке.

Пример:
<pre class="hljs" style="display: block; overflow-x: auto; padding: 0.5em; background-color: rgb(240, 240, 240); color: rgb(68, 68, 68);"><span class="hljs-keyword" style="font-weight: 700;">python</span> main.<span class="hljs-keyword" style="font-weight: 700;">py</span> -link http<span class="hljs-variable" style="color: rgb(188, 96, 96);">s:</span>//bit.ly/<span class="hljs-number" style="color: rgb(136, 0, 0);">3</span>yoRce5
<span class="hljs-built_in" style="color: rgb(57, 115, 0);">count</span> clicks <span class="hljs-number" style="color: rgb(136, 0, 0);">1</span>
</pre>


<h1>Цель проекта</h1>

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
