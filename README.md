# Referral System API

## Описание
Этот проект – реферальная система, реализованная на **Django + Ninja API** с **PostgreSQL** в качестве базы данных.
Проект поддерживает **JWT-аутентификацию**, управление пользователями и реферальными кодами.

Автор проекта: **Малашкин Владимир Олегович**  
Репозиторий на GitHub: [ref_task](https://github.com/faiver-90/ref_task)

---

## 1. Установка и запуск проекта

### 1.1 Клонирование репозитория
```bash
git clone https://github.com/faiver-90/ref_task.git
cd ref_task
```

### 1.2 Создание `.env` файла
Перед запуском создайте файл `.env` в корневой директории на основе `.env_sample`:
```bash
cp .env_sample .env
```

### 1.3 Запуск с Docker Compose
Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build -d
```
После запуска:
- Админ-панель: `http://127.0.0.1:9000/admin/` (логин: `admin`, пароль: `1234`)
- Swagger UI: `http://127.0.0.1:9000/docs`

### 1.4 Остановка контейнеров
```bash
docker-compose down
```

---

## 2. Локальный запуск (без Docker)

### 2.1 Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2.2 Настройка базы данных (PostgreSQL)
Убедитесь, что PostgreSQL запущен и созданы нужные базы данных.

### 2.3 Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2.4 Создание суперпользователя
```bash
python manage.py createsuperuser
```
Введите данные для входа в админку.

### 2.5 Запуск сервера
```bash
python manage.py runserver

## 3. Тестирование API
Перейдите в браузере по адресу:
```
http://127.0.0.1:9000/docs
```
Здесь можно протестировать API без написания кода.

---

## 4. Основные эндпоинты

### 4.1 Аутентификация
| Метод  | URL              | Описание                |
|--------|----------------|-------------------------|
| `POST` | `/auth/token/`  | Получить JWT-токен     |
| `POST` | `/auth/token/refresh/` | Обновить токен    |
| `GET`  | `/auth/validate/` | Проверить токен |

### 4.2 Пользователи
| Метод  | URL              | Описание                     |
|--------|----------------|------------------------------|
| `POST` | `/users/create_user/` | Создать пользователя |
| `PUT`  | `/users/update_user/` | Обновить пользователя |
| `DELETE` | `/users/delete_user/{id}/` | Удалить пользователя |
| `GET`  | `/users/get_user_by_token/` | Получить данные текущего пользователя |

### 4.3 Реферальная система
| Метод  | URL                         | Описание                      |
|--------|-----------------------------|--------------------------------|
| `POST` | `/ref/create/`              | Создать реферальный код       |
| `DELETE` | `/ref/delete/`            | Удалить реферальный код       |
| `GET`  | `/ref/get_by_email/{email}` | Получить рефкод по email |
| `GET`  | `/ref/get_referrals_by_id/{referrer_id}` | Получить список рефералов |

---

## 5. Лицензия
Проект распространяется под **MIT License**.

