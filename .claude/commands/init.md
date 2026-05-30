---
description: "Первичная настройка персонального ассистента. Проводит интервью, создаёт структуру vault, настраивает MCP ktalk, QMD, skills, генерирует профили и конфигурации."
---

# Первичная настройка ассистента

## Предварительная проверка

Проверь, есть ли файл `CLAUDE.md` в корне проекта. Если да — vault уже инициализирован. Спроси пользователя: "Vault уже настроен. Хочешь сбросить настройки и начать заново?"

## Фаза 0: Приветствие

```
👋 Добро пожаловать в настройку Personal Assistant!

Я проведу вас через интервью, создам структуру vault
и настрою интеграции (MCP ktalk, QMD, skills).

Это займёт 5-10 минут.

Начинаем?
```

Ждите ответа пользователя.

## Фаза 1 — Интервью

Проведи интервью с пользователем. Задавай вопросы последовательно, по одному. Записывай ответы.

### Вопрос 1: Компания

"В какой компании вы работаете?"

→ Сохрани как `COMPANY_NAME`

### Вопрос 2: Имя

"Как вас зовут? (Фамилия Имя)"

→ Сохрани как `OWNER_NAME`
→ Сгенерируй `OWNER_ID` по схеме: первая буква имени + фамилия (транслит, латиница, нижний регистр)
   - "Максим Демьянов" → `mdemyanov`
   - "Ольга Петрова" → `opetrova`
   - "John Smith" → `jsmith`
→ Сгенерируй `OWNER_SHORT_NAME`: Фамилия + первая буква имени с точкой
   - "Максим Демьянов" → `Демьянов М.`

### Вопрос 3: Должность

"Какая у тебя должность?"

→ Сохрани как `OWNER_ROLE`
→ Определи домен по должности:
  - Если упоминается "техн", "CTO", "IT", "разработ", "архитект" → `60_DOMAIN/technology`
  - Если "продукт", "CPO", "product" → `60_DOMAIN/product`
  - Если "финанс", "CFO", "бюджет" → `60_DOMAIN/finance`
  - Если "операцион", "COO", "процесс" → `60_DOMAIN/operations`
  - Если "HR", "персонал", "кадр", "people" → `60_DOMAIN/hr`
  - Иначе → спроси: "Какой домен лучше описывает твою зону ответственности?" и предложи варианты
→ Сохрани как `DOMAIN_DIR`

### Вопрос 4: Руководитель

"Кто твой непосредственный руководитель? (Имя и должность, или 'нет' если ты первое лицо)"

→ Если есть — сохрани имя, должность, тип связи = "руководитель"
→ Если "нет" — пропусти

### Вопрос 5: Подчинённые

"Перечисли своих прямых подчинённых (имя и должность на каждой строке, или 'нет')."

Пример ответа:
```
Алексей Муратов — руководитель разработки
Ольга Петрова — руководитель тестирования
```

→ Разбери каждую строку: имя + должность
→ Сгенерируй ID для каждого по той же схеме
→ Сохрани список

### Вопрос 6: Ключевые контакты

"Есть ли другие ключевые люди, с которыми ты регулярно работаешь? (имя, должность, тип связи — коллега/партнёр/заказчик)"

→ Аналогично подчинённым: разбери, сгенерируй ID
→ Если пользователь ответит "нет" или "пока нет" — пропусти

### Вопрос 7: Kontur Talk

Хотите подключить Kontur Talk (ktalk)?
1. Да
2. Нет

Сохраните выбор как `USE_KTALK` (true/false).

## Фаза 2 — Подтверждение

Покажи пользователю сводную таблицу:

```
## Сводка настроек

| Параметр     | Значение                  |
| ------------ | ------------------------- |
| Компания     | {COMPANY_NAME}            |
| Владелец     | {OWNER_NAME} ({OWNER_ID}) |
| Должность    | {OWNER_ROLE}              |
| Домен        | {DOMAIN_DIR}              |
| Руководитель | {имя} или —               |
| Подчинённые  | {N} чел.                  |
| Контакты     | {N} чел.                  |
| MCP ktalk    | {да/нет}                  |
| Vault path   | {текущая директория}      |

### Люди для создания профилей:
{таблица: ID | Имя | Должность | Тип связи}

Всё верно? Продолжить настройку?
```

Дождись подтверждения.

## Фаза 3 — Создание структуры

### 3.1 Создание папок

Выполни:
```bash
bash scripts/setup.sh "." "{DOMAIN_DIR}"
```

### 3.2 Копирование шаблонов

Скопируй все файлы из `templates/` в `90_TEMPLATES/`:
```bash
cp templates/template_*.md 90_TEMPLATES/
cp templates/frontmatter-guide.md 90_TEMPLATES/
```

### 3.3 Генерация CLAUDE.md

Прочитай `presets/base/CLAUDE.md.template`. Замени все плейсхолдеры:

| Плейсхолдер | Значение |
|-------------|----------|
| `{{OWNER_NAME}}` | Из интервью |
| `{{OWNER_ID}}` | Сгенерированный |
| `{{OWNER_ROLE}}` | Из интервью |
| `{{COMPANY_NAME}}` | Из интервью |
| `{{VAULT_NAME}}` | `{COMPANY_NAME}_{OWNER_ROLE}` (транслит, snake_case, без спецсимволов) |
| `{{VAULT_PATH}}` | Абсолютный путь текущей директории |
| `{{DOMAIN_DIR}}` | Определённый домен |
| `{{DATE}}` | Сегодняшняя дата DD.MM.YYYY |
| `{{YEAR}}` | Текущий год |

Запиши результат в `CLAUDE.md` в корне проекта.

### 3.4 Генерация AGENTS.md

Прочитай `presets/base/AGENTS.md.template`. Замени плейсхолдеры. Запиши в `AGENTS.md`.

### 3.5 Генерация vault-config.md

Прочитай `.claude/docs/vault-config.md.template`. Замени плейсхолдеры. Запиши в `.claude/docs/vault-config.md`.

### 3.7 Генерация .mcp.json
**Базовый (без ktalk):**
Прочитай `presets/base/mcp.json.template`. Скопируй как `.mcp.json` в корень.

**С ktalk (если KTALK=true):**
Прочитай `presets/base/mcp_ktalk.json.template`. Скопируй как `.mcp.json` в корень.

Затем скажите пользователю:

```
📝 Файл .mcp.json создан!

Откройте его и замените <ВСТАВЬТЕ_ВАШ_API_КЛЮЧ_ТУДА> на ваш ключ.

Где взять ключ:
1. https://naomi.nau.im/
2. Профиль → Настройки → Аккаунт → API ключ
3. Скопируйте ключ

[.mcp.json](.mcp.json) ← откройте файл

Сохраните и напишите "готово" когда закончите.
```

### 3.8 Генерация settings.local.json

Прочитай `.claude/settings.local.json.template`. Замени `{{VAULT_PATH}}`. Запиши в `.claude/settings.local.json`.

## Фаза 4 — Создание профилей

### 4.1 Профиль владельца

Создай папку `10_PEOPLE/{OWNER_ID}/` и `10_PEOPLE/{OWNER_ID}/1-1/`.

Прочитай `90_TEMPLATES/template_person.md`. Заполни:
- id: `{OWNER_ID}`
- name: `{OWNER_NAME}`
- role: `{OWNER_ROLE}`
- reporting: owner
- status: active

Запиши в `10_PEOPLE/{OWNER_ID}/{OWNER_ID}.md`.

### 4.2 Профиль руководителя (если есть)

Аналогично:
- reporting: external
- В секцию "Подчинённые" добавь ссылку на владельца

### 4.3 Профили подчинённых

Для каждого подчинённого:
1. Создай `10_PEOPLE/{id}/` и `10_PEOPLE/{id}/1-1/`
2. Заполни template_person.md с данными из интервью
3. reporting: direct

### 4.4 Профили контактов

Для каждого контакта:
1. Создай `10_PEOPLE/{id}/`
2. Заполни шаблон
3. reporting: тип из интервью (functional / external)

## Фаза 5 — Создание 00_CORE документов

### 5.1 Скоуп роли

Создай `00_CORE/identity/role_scope.md`:

```markdown
---
type: knowledge
id: role-scope
title: "Скоуп роли: {OWNER_ROLE}"
status: active
---

# Скоуп роли: {OWNER_ROLE}

**Компания:** {COMPANY_NAME}
**Владелец:** [[10_PEOPLE/{OWNER_ID}/{OWNER_ID}|{OWNER_NAME}]]

## Зона ответственности

> Заполни: за что ты отвечаешь?

## Полномочия

> Заполни: что ты можешь решать самостоятельно?

## Ограничения

> Заполни: что требует согласования?

## Ключевые метрики

> Заполни: по каким показателям оценивается твоя работа?
```

### 5.2 Ограничения

Создай `00_CORE/identity/constraints.md`:

```markdown
---
type: knowledge
id: constraints
title: "Ограничения и правила"
status: active
---

# Ограничения и правила

> Заполни: что нельзя делать без согласования? Какие есть красные линии?

## Бюджетные ограничения

-

## Организационные ограничения

-

## Технические ограничения

-
```

### 5.3 Текущие приоритеты

Создай `00_CORE/strategy/current_priorities.md`:

```markdown
---
type: knowledge
id: current-priorities
title: "Текущие приоритеты"
status: active
date: {DATE}
---

# Текущие приоритеты

**Обновлено:** {DATE}

## Приоритет 1

> Заполни

## Приоритет 2

> Заполни

## Приоритет 3

> Заполни
```

### 5.4 Карта стейкхолдеров

Создай `00_CORE/stakeholders/relationship_map.md`:

```markdown
---
type: knowledge
id: relationship-map
title: "Карта связей"
status: active
---

# Карта связей

```mermaid
graph TD
    {MANAGER_ID}["{MANAGER_NAME}<br/>{MANAGER_ROLE}"] --> {OWNER_ID}["{OWNER_NAME}<br/>{OWNER_ROLE}"]
    {OWNER_ID} --> {REPORT_1_ID}["{REPORT_1_NAME}<br/>{REPORT_1_ROLE}"]
    {OWNER_ID} --> {REPORT_2_ID}["{REPORT_2_NAME}<br/>{REPORT_2_ROLE}"]
    ...
```

> Сгенерируй Mermaid-диаграмму на основе данных интервью: руководитель → владелец → подчинённые. Контакты добавь как отдельные связи (пунктирные линии).


## Фаза 6 — Инструменты

### 6.1 qmd

Спроси: "Хочешь установить qmd для семантического поиска по vault? (Требуется Node.js)"

Если да:
Для Windows проверь зависимости, для Mac/Linux пропусти:
```bash
powershell.exe -File "scripts/check-dependencies.ps1"
```
Затем установите qmd:
```bash
bash scripts/install-tools.sh --qmd
```

После установки настрой коллекции:
```bash
qmd collection add ./10_PEOPLE --name {VAULT_NAME}-people --mask "*.md"
qmd collection add ./30_PROJECTS --name {VAULT_NAME}-projects --mask "*.md"
qmd collection add ./20_MEETINGS --name {VAULT_NAME}-meetings --mask "*.md"
qmd collection add ./00_CORE --name {VAULT_NAME}-core --mask "*.md"
qmd collection add ./40_DECISIONS --name {VAULT_NAME}-decisions --mask "*.md"
qmd collection add ./50_KNOWLEDGE --name {VAULT_NAME}-knowledge --mask "*.md"
qmd collection add ./60_DOMAIN --name {VAULT_NAME}-domain --mask "*.md"
```

Затем:
```bash
qmd update
qmd embed
```

## Фаза 7 — Замена плейсхолдеров в командах

Прочитай каждый файл в `.claude/commands/` (кроме init.md). Замени в них:

| Плейсхолдер | Значение |
|-------------|----------|
| `{{VAULT_PATH}}` | Абсолютный путь |
| `{{OWNER_SHORT_NAME}}` | Фамилия + инициал |
| `{{SEARCH_COLLECTION}}` | `{VAULT_NAME}-people` |

Перезапиши файлы с актуальными значениями.

## Фаза 8 — Финальный отчёт

Выведи итоговый отчёт:

```
## Настройка завершена!

### Создано
- {N} папок в структуре vault
- {N} профилей людей
- {N} шаблонов в 90_TEMPLATES/
- CLAUDE.md, AGENTS.md
- Документы в 00_CORE/

### Настроено
- Команды: /new-1-1, /new-decision, /find-person, /kb-stats, /meeting-debrief, /new-project
- Поиск: qmd / файловый
- Субагенты: researcher, meeting-processor, document-creator, writer, analyst

### Следующие шаги
0. Ознакомься с памяткой по безопасности - SECURITY.md
1. Заполни `00_CORE/identity/role_scope.md` — твои полномочия
2. Заполни `00_CORE/strategy/current_priorities.md` — приоритеты
3. Попробуй: `/find-person {первый_подчинённый}`
4. Попробуй: `/new-1-1`
5. (Опционально) Открой папку как Obsidian vault
```
