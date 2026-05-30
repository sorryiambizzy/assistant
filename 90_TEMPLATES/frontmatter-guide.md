---
type: knowledge
id: frontmatter-guide
title: "Руководство по Frontmatter"
status: active
domain: general
---

# Руководство по Frontmatter

## Универсальные поля

```yaml
---
type: ""           # person | meeting | project | decision | knowledge | memo
id: ""             # уникальный идентификатор
title: ""
status: ""         # draft | active | completed | archived
date: YYYY-MM-DD
domain: ""         # technology | finance | product | operations | general
tags: []
related: []        # WikiLinks на связанные документы
owner: ""          # WikiLink на person
---
```

## Подтипы

**Для встреч (meeting):**
- `1-1` — встреча один на один
- `committee` — комитет
- `standup` — регулярный синхрон
- `session` — стратегическая сессия

**Для решений (decision):**
- `record` — запись решения
- `policy` — политика
- `journal-entry` — запись в Decision Journal

## Примеры

### Профиль человека
```yaml
---
type: person
id: "amuratov"
name: "Алексей Муратов"
role: "Руководитель разработки"
reporting: direct
status: active
---
```

### 1-1 встреча
```yaml
---
type: 1-1
person: "Алексей Муратов"
date: 2026-02-20
status: done
---
```

### Проект
```yaml
---
type: project
id: "project-alpha"
title: "Проект Альфа"
status: active
priority: high
---
```

### Решение
```yaml
---
type: decision
id: "DEC-0001"
title: "Выбор платформы"
date: 2026-02-20
status: accepted
---
```
