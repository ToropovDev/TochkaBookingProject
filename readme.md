# Проект по записи на волейбольные игры.
## Сделан в рамках курса "Технологии современных решений на базе Python" (АО Точка)

## Используемые технологии
- Python
- FastAPI
- PostgreSQL
- Redis
- celery
- fastapi-users
- Pydantic
- SQLalchemy
- APScheduler
- iCalendar
- React
- Vite
- Ant Design

## Функционал бекенда 
Написанный сервис позволяет конечному пользователю зарегистрироваться в системе, подтвердить свою почту с помощью кода и войти в систему.
Так же пользователь можно восстановить забытый пароль так же через почту.

Далее пользователь может создать свою команду, как пустую так и заполненную, где каждый игрок занимают конкретную игровую позицию.
Используя созданные команды пользователь может создать игру, указав название, место, время, уровень и статус игры, участвующие команды.

Также в момент создания игры пользователь может оставить донат создателю сервиса (пока только тестовые платежи ЮКасса, для тестирования платежей использовать карту 5555555555554477 и любые данные для даты и кода)

После создания игры пользователю на почту приходит .ics-файл, чтобы он мог добавить в свой календарь запись об этой игре. Также приходит напоминание об игре за 2 часа до ее начала.

Также пользователь может посмотреть созданные другими юзерами игры, состав участвующих команд и записаться в любую из них.

Для всех сущностей в проекте (пользователи, команды, игры, платежи) реализован CRUD.

## Функционал фронтенда
На фронтенд-часть приложения добавлена не вся функциональность, однако самая основная доступна:
- регистрация и подтверждение аккаунта
- вход
- создание, изменение и удаление команд
- изменение профиля
- создание, изменение и удаление игр 
- запись на игру

## Деплой приложения
Для деплоя приложения был использован Docker. Python, React, celery, Redis и PostgreSQL запущены в отдельных контейнерах. Сервис загружен на арендованный сервер, который находится в Амстердаме, поэтому, возможно, для входа на сайт понадобится VPN.