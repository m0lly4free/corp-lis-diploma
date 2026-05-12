АО «Корпорация ЛИС» — Корпоративный веб-портал
================================================================================

Информационный ресурс компании по заготовке и переработке лома черных и
цветных металлов. Проект разработан с соблюдением требований к адаптивности,
безопасности и управляемости контента.

Версия: 9.3.6p3 moded
Дата обновления: 06.05.2026
Ветка: dev


СОДЕРЖАНИЕ
================================================================================
1. Структура проекта
2. Технологический стек
3. Быстрый старт
4. Настройка окружения
5. Тестирование
6. Управление контентом
7. Деплой и SSL
9. Примечание (!!!)


1 - СТРУКТУРА ПРОЕКТА
================================================================================

Корень проекта (corp-lis-diploma/):
  |-- api/                 # API эндпоинты (Django REST Framework)
  |-- backup/              # Скрипты резервного копирования БД
  |-- backups/             # Папка для хранения бэкапов
  |-- contacts/            # Приложение: форма обратной связи
  |-- core/                # Общие утилиты, миксины, базовые классы
  |-- corp_lis/            # Настройки Django (settings/, urls.py, wsgi.py)
  |-- locale/              # Файлы локализации (переводы)
  |-- media/               # Загружаемые файлы (изображения услуг/новостей)
  |-- news/                # Приложение: новостная лента
  |-- nginx/               # Конфигурация Nginx для продакшена
  |-- pages/               # Приложение: статические страницы (Главная, О нас)
  |-- services/            # Приложение: каталог услуг
  |-- static/              # CSS, JS, шрифты, иконки
  |-- templates/           # HTML-шаблоны (base.html, includes/, страницы)
  |-- tests/               # Тесты
  |-- users/               # Приложение: пользователи и авторизация

Корневые файлы:
  |-- manage.py            # CLI управления Django
  |-- docker-compose.yml   # Оркестрация контейнеров (web, db, nginx, certbot)
  |-- Dockerfile           # Инструкция сборки образа приложения
  |-- requirements.txt     # Зависимости Python
  |-- package.json         # Зависимости Node.js (Tailwind, сборка статики)
  |-- tailwind.config.js   # Настройка TailwindCSS
  |-- DEPLOY.md            # Подробная инструкция по деплою
  |-- README.txt           # Этот файл
  |-- .gitignore           # Исключаемые файлы для Git


2 - ТЕХНОЛОГИЧЕСКИЙ СТЕК
================================================================================

Backend:
  - Python 3.11
  - Django 4.2+
  - Django REST Framework (API)
  - PostgreSQL 15 (база данных)
  - Redis (кэширование, очереди)

Frontend:
  - HTML5, CSS3, Vanilla JavaScript
  - TailwindCSS (сборка через npm)
  - Адаптивная верстка (mobile-first)

Инфраструктура:
  - Docker, Docker Compose
  - Nginx (reverse proxy, статика, SSL)
  - Gunicorn (WSGI-сервер для Django)
  - Let's Encrypt / Certbot (SSL-сертификаты)

Безопасность:
  - CSRF-токены, экранирование XSS
  - Honeypot-защита форм от спама
  - django-axes (защита от brute-force)
  - Валидация данных на уровне моделей и форм

Тесты:
  - Django Test Framework
  - SQLite (для мгновенного прогона теста)
  - Django Test Client (виртуальный браузер)


3 - БЫСТРЫЙ СТАРТ
================================================================================

Требования:
  - Docker Desktop (Windows/macOS) или Docker Engine + Compose (Linux)
  - Git

Шаги:

1. Клонирование:
   git clone -b dev https://github.com/m0lly4free/corp-lis-diploma
   cd corp-lis-diploma

2. Настройка окружения:
   Скопируйте пример и отредактируйте переменные:
   (создайте файл .env в корне, если его нет)

3. Запуск:
   docker-compose up -d --build

4. Инициализация:
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   docker-compose exec web python manage.py collectstatic --noinput

5. Готово:
   Сайт: http://localhost
   Админка: http://localhost/corp-lis-secure-portal/


4 - НАСТРОЙКА ОКРУЖЕНИЯ (.env)
================================================================================

Обязательные переменные:

Режим отладки (False для продакшена)
- DEBUG=False

Секретный ключ (сгенерируйте через secrets.token_urlsafe(50))
- SECRET_KEY=ваш-ключ-здесь

Разрешенные домены
ALLOWED_HOSTS=localhost,127.0.0.1,corp-lis.ru

База данных
- DB_NAME=corplis_db
- DB_USER=corplis_admin
- DB_PASSWORD=надежный-пароль
- DB_HOST=db
- DB_PORT=5432

Email (для отправки заявок)
- EMAIL_HOST=smtp.yandex.ru
- EMAIL_PORT=587
- EMAIL_USE_TLS=True
- EMAIL_HOST_USER=noreply@corp-lis.ru
- EMAIL_HOST_PASSWORD=пароль-приложения

Кэширование (опционально)
- REDIS_URL=redis://redis:6379/1


5 - ТЕСТИРОВАНИЕ
================================================================================

Запуск тестов:

# Команада запуска всех тестoв проекта
docker-compose exec web python manage.py test tests --settings=corp_lis.settings.test --verbosity=1

# Выводы последнего теста (05.05.26 v9.2.6p3 (no commit) | 16:44 UTC+3)
```
(venv) PS C:\Users\---\corp-lis-diploma> docker-compose exec web python manage.py test tests --settings=corp_lis.settings.test --verbosity=1
time="2026-05-05T16:44:29+03:00" level=warning msg="C:\\Users\\---\\corp-lis-diploma\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
Found 53 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....WARNING Not Found: /nonexistent-page-12345/
.........WARNING Not Found: /services/
....INFO Попытка отправки уведомления для обращения #1. Получатель: noreply@corp-lis.ru, Тема: Новое обращение с формы контактов
INFO Уведомление успешно отправлено для обращения #1
Critical error saving message: 'contacts' is not a registered namespace
..........WARNING Not Found: /static/css/main.css
......Validation failed for IP 127.0.0.1
.WARNING Forbidden (CSRF cookie not set.): /contacts/
.....ERROR API error in ServiceListView: Non-relational field given in select_related: 'category'. Choices are: (none)
ERROR Internal Server Error: /api/services/
..............
----------------------------------------------------------------------
Ran 53 tests in 0.623s

OK
Destroying test database for alias 'default'...
```
*ПОЯСНЕНИЕ*
Вы можете игнорировать строки вроде WARNING Not Found, Forbidden или Validation failed. Это нормальное поведение:
* Тесты специально запрашивают несуществующие страницы, чтобы проверить, что сайт возвращает ошибку 404 (что и фиксируется как Not Found).
* Тесты проверяют защиту от спама/CSRF, получая Forbidden, что подтверждает безопасность.


# Покрытые требования:
1. Модульное тестирование: Проверка корректности работы моделей (Service, News) и форм (ContactForm).
2. Функциональное тестирование: Проверка доступности основных страниц сайта и административной панели.
3. Безопасность: Проверка защиты от CSRF-атак и корректности ограничений доступа для разных ролей пользователей.
4. Обработка ошибок: Корректная обработка несуществующих запросов (404 Not Found) и защита от невалидных данных.

6 - УПРАВЛЕНИЕ КОНТЕНТОМ
================================================================================

Админ-панель: /corp-lis-secure-portal/

Добавление услуги:
1. Раздел "Услуги" -> "Добавить"
2. Заполните: Название, Slug (URL)(заполнение автоматически), Краткое описание, Полное описание
3. Загрузите изображение (опционально, до 5 МБ)
4. Поставьте галочку "Опубликовано" (is_active)
5. Сохраните

Добавление новости:
1. Раздел "Новости" -> "Добавить"
2. Укажите заголовок, slug, краткое и полное описание
3. Прикрепите изображение для превью
4. Установите дату публикации и статус
5. Сохраните

Форма обратной связи:
- Все заявки автоматически отправляются на EMAIL_HOST_USER
- Защита от спама: скрытые поля (honeypot) + CSRF
- Валидация: обязательные поля, формат email, длина сообщения


7 - ДЕПЛОЙ И SSL
================================================================================

Подготовка сервера (Ubuntu 22.04+):
1. Установите Docker и Docker Compose
2. Откройте порты 80 (HTTP) и 443 (HTTPS)
3. Настройте домен (A-запись на IP сервера)

Развертывание:
1. Скопируйте проект на сервер
2. Настройте .env с продакшен-параметрами
3. В docker-compose.yml укажите ваш домен в секции nginx
4. Запустите: docker-compose -f docker-compose.yml up -d

Получение SSL-сертификата (Let's Encrypt):
1. Выполните команду:
   docker-compose run --rm certbot certonly --webroot \
     --webroot-path=/var/www/certbot \
     -d corp-lis.ru -d www.corp-lis.ru \
     --email admin@corp-lis.ru --agree-tos --no-eff-email

2. Перезапустите контейнеры:
   docker-compose up -d

3. Автообновление сертификата настроено через cron в контейнере certbot

Подробнее: см. файл DEPLOY.md в корне проекта (пока не готов)


ПРИМЕЧАНИЕ
================================================================================

Дипломная работа на 06.05.2026 находится на финальной стадии разработки и некоторые функции могут работать не корректно. 


*А ТАК ЖЕ*:
* В демонстрационных целях используется самоподписанный SSL-сертификат. В производственной среде будет установлен сертификат Let's Encrypt с автоматическим обновлением через certbot.

Установка Let's Encrypt (production)
Замените corp-lis.ru на ваш домен в docker-compose.yml и nginx.conf
Выполните команду получения сертификата: docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d corp-lis.ru -d www.corp-lis.ru --email admin@corp-lis.ru --agree-tos --no-eff-email
Перезапустите: docker-compose up -d