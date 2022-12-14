# Watchdog

**Watchdog** сервис предназначен для решения задачи проверки работаспособности развёрнутых и поддерживаемых сайтов. Проверка происходит в виде запросов ``GET`` к главным страницам сайтов.

### Проверка в три этапа `GET` запросом:

1. Есть ли вообще в пространстве имён `DNS` этот сайт.
2. Отдаёт ли ответ `200` на `GET` запрос.
3. Получение `контрольной фразы` с главной страницы сайта.

`контрольная фраза` - как правило уникальный редко изменяемый реквизит. Например, номер телефона, адрес электронной почты или георгафический адрес редакции.

### Параметры

**Параметры** все параметры представлены в `settings.py`:

1. `TOKEN` - token телеграм бота. Пример "5124231563:AAE3723-HrMJP7pmBMRM_xc8wByZsN9dfzA".
2. `CHAT_ID` - идентификатор чата. Пример 422944053.
3. `CHECK_BOT_SEC` - период в секундах проверки работоспособности сервиса `watchdog`. Сервис отправляет сообщения `I'm alive` в чат бота, для уверенности, что сервис в работоспособном состоянии. Пример 3600.
4. `data` - словарь со списком данных проверяемых сайтов:
    - `host` - `url` сайта. Пример "https://kvgazeta.ru".
    - `check_text` - текст, который нужно получить при проверке с главной страници сайта. Пример "662720, п. Шушенское, ул. Ленина, 65".
    - `check_times` - количество раз проверка сайта должна получить отрицательный результат, после чего увовень логирования становиться `CRITICAL` и отправляется сообщение, что сайт не доступен в чат телеграм бота. Пример 3.
    - `check_period_sec` - период проверки сайта в секундах. Пример 60.

### Уровни логирования

1. `INFO` - проверка сайта прошла успешно. Всё нормально.
2. `ERROR` - сайт не прошел проверку, но количество проверок с отрицательным результатом не превышает указанных в `check_times`.
3. `CRITICAL` - количество проверок с отрицательным результатом равно или превышает указанных в `check_times`. При этом отправляется сообщение в чат телеграм бота.

### Создание и запуск docker контейнера

```shell
docker-compose build
docker-compose up -d
```

### Создание телеграм бота

С помощью бота `@BotFather` создать нового бота:

```shell
/newbot
```
`TOKEN` сообщается после успешного создания нового бота.

### Определение `CHAT_ID`

Пример:

```shell
https://api.telegram.org/bot5124231563:AAE3723-HrMJP7pmBMRM_xc8wByZsN9dfzA/getUpdates
```
где "5124231563:AAE3723-HrMJP7pmBMRM_xc8wByZsN9dfzA" это `TOKEN`
