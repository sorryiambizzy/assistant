---
type: person
id: "ibelova"
name: "Белова Ирина"
role: "Teamlead аналитиков мобильного приложения Naumen SMP"
team: "Analytics"
reporting: direct
since: 2026-03-18
status: active
domain: technology
tags:
  - person
---

# Белова Ирина

**Должность:** Teamlead аналитиков мобильного приложения Naumen SMP
**Подчинение:** Прямое
**Команда:** Analytics

---

## Зона ответственности

-

---

## Подчинённые

| Имя | Роль | Примечание |
|-----|------|------------|
| | | |

---

## Текущие цели

| Цель | Срок | Статус |
|------|------|--------|
| | | |

---

## Сильные стороны

-

---

## Зоны развития

-

---

## Заметки

>

---

## Открытые договорённости

| Дата | Договорённость | Срок | Статус |
|------|----------------|------|--------|
| | | | ⬜ |

---

## Вопросы для следующей 1-1

-

---

## Участие в проектах

```dataview
TABLE WITHOUT ID
  link(file.link, id) as "Проект",
  title as "Название",
  status as "Статус"
FROM "30_PROJECTS/active"
WHERE type = "project" AND contains(file.outlinks, this.file.link)
SORT status ASC
```

---

## История 1-1

```dataview
TABLE date as "Дата", status as "Статус"
FROM "10_PEOPLE"
WHERE contains(file.path, this.file.folder) AND type = "1-1"
SORT date DESC
LIMIT 10
```

---

## История изменений

| Дата | Изменения |
|------|-----------|
| 18.03.2026 | Создание профиля |
