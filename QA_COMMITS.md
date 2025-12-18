# Инструкция по коммитам QA-артефактов

## Структура файлов для коммита

```
MedSite/
├── ai-rules/
│   └── qa_ulan.md          # Правила QA роли для AI
├── QA_CHECKLIST.md          # Чек-лист тестов
├── WORKFLOW.md              # Документация workflow
├── tests/
│   └── e2e/
│       └── .gitkeep        # Папка для E2E тестов
├── .gitignore              # Git ignore файл
└── QA_COMMITS.md           # Эта инструкция
```

## Команды для коммита

### 1. Проверка статуса
```bash
git status
```

### 2. Создание ветки (если еще не создана)
```bash
git checkout -b qa/ulan-e2e
```

### 3. Коммиты маленькими порциями

#### Коммит 1: QA правила
```bash
git add ai-rules/qa_ulan.md
git commit -m "chore: add qa ai-rules"
```

#### Коммит 2: QA чеклист и workflow
```bash
git add QA_CHECKLIST.md WORKFLOW.md
git commit -m "docs: add QA checklist and workflow"
```

#### Коммит 3: Структура для тестов
```bash
git add tests/e2e/.gitkeep .gitignore
git commit -m "chore: add e2e tests directory structure"
```

### 4. Пуш в репозиторий
```bash
git remote add origin https://github.com/Deathstroke97/idoc.git
# или если remote уже есть:
git push -u origin qa/ulan-e2e
```

## Альтернатива: один коммит (если нужно быстро)

```bash
git add ai-rules/ QA_CHECKLIST.md WORKFLOW.md tests/ .gitignore
git commit -m "chore: add QA artifacts and structure"
git push -u origin qa/ulan-e2e
```

## Следующие шаги

После пуша в репозиторий:
1. Дождаться появления кода проекта
2. Выполнить Шаг A — Инвентаризация проекта
3. Выполнить Шаг C — Написание E2E тестов
4. Сделать коммит с тестами: `test: add e2e smoke tests`

