---
type: meta
title: "Dashboard"
tags: [meta, dashboard]
---

# naumen_mobile_technology_manager — Dashboard

**Владелец:** [[10_PEOPLE/epodkin/epodkin|Подкин Евгений]]
**Роль:** Менеджер мобильных технологий, Naumen

---

## Быстрые действия

- `/find-person` — найти информацию о человеке
- `/new-1-1` — создать запись 1-1 встречи
- `/new-decision` — зафиксировать решение
- `/new-project` — создать проект
- `/kb-stats` — статистика базы знаний
- `/meeting-debrief` — обработать транскрипт встречи

---

## Люди

```dataview
TABLE role as "Должность", status as "Статус"
FROM "10_PEOPLE"
WHERE type = "person"
SORT name ASC
```

---

## Активные проекты

```dataview
TABLE title as "Название", status as "Статус", priority as "Приоритет"
FROM "30_PROJECTS/active"
WHERE type = "project"
SORT priority ASC
```

---

## Последние решения

```dataview
TABLE title as "Решение", date as "Дата", status as "Статус"
FROM "40_DECISIONS"
WHERE type = "decision"
SORT date DESC
LIMIT 10
```

---

## Текущие приоритеты

> Заполни в `00_CORE/strategy/current_priorities.md`
