---
description: Постобработка встреч — извлекает договорённости, решения, задачи из транскриптов
---

# Постобработка встреч

## Инструкции

Загрузи и выполни workflow из глобального skill meeting-debrief.

Параметры vault — в CLAUDE.md (секция "Контекст для skills") и `.claude/docs/vault-config.md`.

## Архивация транскрипта

После успешной обработки:

1. **Переименуй файл:**
   ```
   {YYYY-MM-DD}_{meeting_type}_{title}.{ext}
   ```
   meeting_type: `1-1`, `committee`, `standup`, `session`, `other`

2. **Перенеси в архив:**
   ```
   99_ARCHIVE/transcripts/{YYYY}/
   ```

3. **Сообщи** путь к архивированному файлу.
