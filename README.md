Для решения можно использовать любой из следующих фреймворков: (Django, Tornado, Flask, Pyramid, Falcon, AioHTTP, Sanic).

Выбранных вами библиотек может не быть на компьютере проверяющего, поэтому укажите все зависимости в отдельном файле. Если вы достаточно хорошо знакомы с Docker, то можете написать Dockerfile к вашему приложению, docker-compose конфигурационный файл и упаковать все необходимое в контейнеры, где все уже будет установлено, а ваш код собран и готов к запуску. Это идеальный вариант.

После проверки задания мы обязательно сообщим вам о нашем решении. Код тестового задания не планируется использовать в коммерческих целях.

## Описание

Необходимо создать приложение, которое будет периодически парсить главную страницу [Hacker News](https://news.ycombinator.com/), вытягивая из нее **список постов** и сохраняя в базу данных.
А еще приложение должно иметь HTTP API с всего одним методом (**GET** /posts), с помощью которого можно будет получить **список всех доступных (собранных) новостей.**
По каждой новости необходимо иметь заголовок и URL, а также время, когда она была сохранена в БД. Достаточно **сохранять только 30 новостей** и приходить за новыми через определенный интервал времени, либо по-требованию.
API метод для получения списка новостей на запрос:

`curl -X GET [http://localhost:8000/posts](http://localhost:8000/posts)`

Результат список новостей в формате JSON

`[ {"id": 1, "title": "Announcing Rust 1.33.0", "url": "[https://example.com](https://example.com/)", "created": "ISO 8601"}, {"id": 2, "title": "Redesigning GitHub Repository Page", "url": "[https://example.com](https://example.com/)", "created": "ISO 8601"}]`

Должна работать сортировка по заданному атрибуту, по возрастанию и убыванию.

`curl -X GET [http://localhost:8000/posts?order=title](http://localhost:8000/posts?order=title)`

Так же клиент должен иметь возможность **запросить подмножество данных, указав offset и limit**. Пусть по-умолчанию API возвращает 5 постов.
`curl -X GET http://localhost:8000/posts?offset=10&limit=10`

Разумеется, клиент может **указать и сортировку, и лимит одновременн**о.
Подумайте о том, что должно произойти, если клиент передал несуществующий атрибут для сортировки. Или параметр limit слишком большой? А может быть вообще отрицательный? Что API сделает в таком случае?

## Требования

- Инструкции по запуску приложения должны находится в README
- Ссылка на github репозиторий с решением
- Ссылка на развернутое приложение доступное публично
- Использовать docker
- Код должен быть покрыт тестами. Вы можете использовать любую библиотеку (unittest, nose, pytest)