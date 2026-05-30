---
description: Статистика и обзор базы знаний
---

# Статистика базы знаний

## Алгоритм

### 1. Общая статистика

Если qmd доступен:
```
qmd_status
```

Если нет:
```
Glob: **/*.md → подсчитать общее количество
```

### 2. По типам документов

```
Grep: pattern="type: person", path="10_PEOPLE/"
Grep: pattern="type: 1-1", path="10_PEOPLE/"
Grep: pattern="type: project", path="30_PROJECTS/"
Grep: pattern="type: decision", path="40_DECISIONS/"
Grep: pattern="type: meeting", path="20_MEETINGS/"
```

### 3. Структура vault

Загрузи `.claude/docs/kb-structure.md` для справки.

## Формат ответа

```markdown
## Статистика базы знаний

### Общие показатели
| Метрика | Значение |
|---------|----------|
| Всего документов | {total} |
| Последнее обновление | {date} |

### По типам
| Тип | Количество |
|-----|------------|
| person | {n} |
| 1-1 | {n} |
| project | {n} |
| decision | {n} |
| meeting | {n} |
```
