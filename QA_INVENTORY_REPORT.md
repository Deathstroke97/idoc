# Отчет инвентаризации проекта — iDoc

**Дата:** 2025-01-XX  
**QA Engineer:** ulan  
**Репозиторий:** https://github.com/Deathstroke97/idoc

---

## 1. Стек проекта

### Backend
- **Фреймворк:** FastAPI 0.115.13
- **ORM:** SQLAlchemy 2.0.36
- **База данных:** SQLite (файл `backend/database.sqlite3`, создается автоматически)
- **Сервер:** Uvicorn 0.34.0
- **Язык:** Python 3.8+

### Frontend
- ❌ **Отсутствует** (не реализован)

### AI компоненты
- ❌ **Отсутствуют** (не реализованы)

---

## 2. Как запускать проект

### Команды запуска

```bash
# 1. Создать виртуальное окружение (рекомендуется)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 2. Установить зависимости
pip install -r backend/requirements.txt

# 3. Запустить сервер
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Доступные URL после запуска
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Переменные окружения
- ❌ Не требуются (нет `.env` файла)
- База данных создается автоматически при первом запуске

---

## 3. Структура проекта

```
idoc/
├── backend/
│   ├── __init__.py
│   ├── main.py              # Основной файл приложения (FastAPI app, модели, endpoints)
│   ├── seed_data.py         # Данные для автозаполнения (10 клиник, 20 врачей)
│   ├── requirements.txt     # Зависимости Python
│   ├── backend.md           # Документация backend
│   └── database.sqlite3     # SQLite БД (создается автоматически)
├── README.md                # Основная документация проекта
├── Agents.md                # Заметки для агентов
├── .gitignore               # Git ignore файл
└── (QA артефакты)
    ├── ai-rules/
    ├── QA_CHECKLIST.md
    ├── WORKFLOW.md
    └── tests/e2e/
```

---

## 4. API Endpoints (Backend)

### `GET /clinics`
- **Описание:** Список клиник с врачами
- **Query параметры:**
  - `q` (optional) — поиск по названию клиники
- **Response:** `List[ClinicOut]`
  - `id`, `name`, `doctors: List[DoctorOut]`
- **Пример:** `GET /clinics?q=Aurora`

### `GET /doctors`
- **Описание:** Список врачей
- **Query параметры:**
  - `q` (optional) — поиск по имени врача
  - `clinic_id` (optional) — фильтр по клинике
- **Response:** `List[DoctorOut]`
  - `id`, `name`, `clinic_id`
- **Пример:** `GET /doctors?clinic_id=1&q=Alex`

### `POST /make-appointmet` ⚠️ (опечатка в названии сохранена)
- **Описание:** Создание записи на прием
- **Body:** `AppointmentCreate`
  - `clinic_id: int` (required)
  - `doctor_id: int` (required)
  - `date: str` (required) — дата приема
  - `time: str` (required) — время приема
  - `user_name: str` (required) — имя пользователя
  - `user_phone: str` (required) — телефон пользователя
- **Response:** `AppointmentOut` (201 Created)
- **Валидация:**
  - Проверяет существование клиники (404 если не найдена)
  - Проверяет существование врача (404 если не найден)
  - Проверяет что врач принадлежит клинике (400 если нет)

---

## 5. Модели данных (SQLAlchemy)

### `Clinic`
- `id: int` (PK)
- `name: str` (unique)
- `doctors: List[Doctor]` (relationship)

### `Doctor`
- `id: int` (PK)
- `clinic_id: int` (FK → Clinic.id, CASCADE delete)
- `name: str`
- `clinic: Clinic` (relationship)

### `Appointment`
- `id: int` (PK)
- `clinic_id: int` (FK → Clinic.id, CASCADE delete)
- `doctor_id: int` (FK → Doctor.id, CASCADE delete)
- `date: str` — дата приема
- `time: str` — время приема
- `user_name: str` — имя пользователя
- `user_phone: str` — телефон пользователя

---

## 6. Тестовые данные

### Автозаполнение (seed data)
При первом запуске, если клиник нет, создается:
- **10 клиник** (из `CLINIC_NAMES` в `seed_data.py`)
- **20 врачей на каждую клинику** (из `DOCTOR_NAMES` в `seed_data.py`)
- Итого: **10 клиник × 20 врачей = 200 врачей**

### Примеры клиник:
- Aurora Health Clinic
- Green Valley Medical
- Sunrise Wellness Center
- и т.д.

### Примеры врачей:
- Dr. Alex Morgan
- Dr. Jamie Rivera
- Dr. Taylor Chen
- и т.д.

---

## 7. Что уже есть для тестов

### Существующие тесты
- ❌ **Нет** (тесты отсутствуют)

### Тестовые данные
- ✅ Есть seed data для автозаполнения
- ✅ База данных создается автоматически

### Test IDs / Селекторы
- ❌ **Нет frontend** — селекторы не применимы
- ✅ **API endpoints** — можно тестировать через HTTP запросы

---

## 8. Важные страницы/эндпоинты для тестирования

### Backend API (P0 — критично)
1. ✅ `GET /clinics` — список клиник
2. ✅ `GET /doctors` — список врачей
3. ✅ `POST /make-appointmet` — создание записи

### Frontend (P0 — критично, но отсутствует)
- ❌ Список клиник (страница)
- ❌ Список услуг (страница) — **НЕ РЕАЛИЗОВАНО**
- ❌ Список врачей (страница)
- ❌ Форма записи (страница)

### AI компоненты (P1 — опционально, но отсутствует)
- ❌ Чат-бот
- ❌ Fallback механизм

---

## 9. Отсутствующий функционал (из требований)

### Обязательный функционал (без AI):
- ✅ Список клиник (API есть, UI нет)
- ❌ **Услуги** — **НЕ РЕАЛИЗОВАНО** (нет модели, нет endpoint)
- ✅ Врачи (API есть, UI нет)
- ✅ Запись/форма (API есть, UI нет)

### AI функционал:
- ❌ Чат-бот
- ❌ Fallback механизм

---

## 10. Рекомендации для тестирования

### Backend API тесты (можно написать сейчас)
1. **Unit тесты** для моделей и валидации
2. **API тесты** (pytest + httpx) для всех endpoints
3. **Интеграционные тесты** для проверки связей между моделями

### E2E тесты (требуют frontend)
- ⏳ **Ожидание frontend** — после появления UI можно писать E2E тесты (Playwright)

### Что тестировать в API:
- ✅ `GET /clinics` — возвращает список, поиск работает
- ✅ `GET /doctors` — возвращает список, фильтры работают
- ✅ `POST /make-appointmet` — создание записи, валидация ошибок
- ✅ Обработка ошибок (404, 400)

---

## 11. Следующие шаги

1. ✅ **Инвентаризация завершена**
2. ⏳ **Запустить проект** и проверить работоспособность
3. ⏳ **Написать API тесты** (pytest + httpx)
4. ⏳ **Дождаться frontend** для E2E тестов
5. ⏳ **Обновить QA_CHECKLIST.md** с учетом реальной структуры проекта

---

**Статус:** ✅ Инвентаризация завершена  
**Следующий шаг:** Запуск проекта и проверка работоспособности

