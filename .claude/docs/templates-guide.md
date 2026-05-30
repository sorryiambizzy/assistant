# Шаблоны и создание документов

## Доступные шаблоны (90_TEMPLATES/)

| Файл | Назначение |
|------|-----------|
| `template_1-1.md` | Записи 1-1 встреч |
| `template_person.md` | Профиль сотрудника |
| `template_decision.md` | Запись решения |
| `template_project.md` | Карточка проекта |
| `template_committee_meeting.md` | Протокол комитета |
| `template_memo.md` | Служебная записка |
| `template_methodology.md` | Методология |

## Типичные задачи

| Задача | Шаблон | Куда сохранять |
|--------|--------|---------------|
| Записать 1-1 | `template_1-1.md` | `10_PEOPLE/{id}/1-1/{YYYY-MM-DD}.md` |
| Создать решение | `template_decision.md` | `40_DECISIONS/records/DEC-{NNNN}.md` |
| Новый проект | `template_project.md` | `30_PROJECTS/active/{id}/{id}.md` |
| Профиль человека | `template_person.md` | `10_PEOPLE/{id}/{id}.md` |
| Протокол комитета | `template_committee_meeting.md` | `20_MEETINGS/committees/{id}/{date}.md` |

## YAML frontmatter — обязателен

```yaml
---
type: person | meeting | project | decision | knowledge | memo
id: "идентификатор"
title: "Название"
status: draft | active | completed | archived
date: YYYY-MM-DD
domain: general
---
```

Подробное руководство: `90_TEMPLATES/frontmatter-guide.md`
