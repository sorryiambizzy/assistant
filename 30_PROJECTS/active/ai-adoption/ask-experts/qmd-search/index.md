---
type: project_subtrack
id: "ai-adoption-ask-experts-qmd-search"
title: "Подтрек: qmd-search — индексированный поиск по документации Naumen"
parent: "[[30_PROJECTS/active/ai-adoption/ask-experts/index|Ask Experts]]"
grandparent: "[[30_PROJECTS/active/ai-adoption/ai-adoption|AI-Adoption]]"
status: discovery
owner: "[[10_PEOPLE/epodkin/epodkin|Подкин Евгений]]"
start_date: 2026-06-03
target_date: ""
domain: technology
tags:
  - project-subtrack
  - ai
  - ask-experts
  - docs-search
  - qmd
  - naumen-docs
---

# Подтрек: qmd-search — индексированный поиск по документации Naumen

**Родительский трек:** [[30_PROJECTS/active/ai-adoption/ask-experts/index|Ask Experts]]
**Проект:** [[30_PROJECTS/active/ai-adoption/ai-adoption|AI-Adoption]]

---

## Фокус подтрека

Альтернативная реализация поиска по документации Naumen для аналитиков и сотрудников технической поддержки. Параллельна BPM-плагину Антона (который встроен в SMP и работает «изнутри» процесса асков) — этот подтрек делает поиск **извне**: локальный индекс по публичной доке, доступный через Claude Code skill.

**Зачем параллельная реализация:**
- BPM-плагин работает в контексте конкретного аска внутри SMP — короткий цикл, ответ оператору.
- qmd-skill — для аналитика/поддержки в IDE/CLI: исследование, написание ответов, ревью требований, обучение.
- Это разные UX и разная аудитория. Сравнение качества и боли — отдельная задача (см. tasks.md).

**Гипотеза:** связка `публичная дока Naumen → markdown-чанки → qmd hybrid index → Claude Code skill` даёт аналитику быстрый цитируемый ответ с прямой ссылкой на источник, при затратах на запуск в один день и поддержку — раз в квартал.

---

## Критерии успеха (discovery → active)

- [ ] Skill отвечает на 8 из 10 типичных вопросов поддержки/аналитики со score ≥80% (BM25) и точной цитатой из источника.
- [ ] Качество сравнимо или лучше, чем у BPM-плагина Антона на пересекающихся кейсах.
- [ ] Один из стейкхолдеров (Даша Тимганова или другой аналитик) использует skill в реальной работе минимум неделю.
- [ ] Понятен путь раскатки на команду (skill / плагин / shared MCP).

---

## Команда подтрека

| Роль | Человек | Ответственность |
|------|---------|-----------------|
| Ведущий | [[10_PEOPLE/epodkin/epodkin\|Подкин Евгений]] | Скилл, пайплайн, валидация |
| Параллельный пилот | [[10_PEOPLE/astolbov/astolbov\|Столбов Антон]] + [[10_PEOPLE/dtimganova/dtimganova\|Тимганова Даша]] | BPM-плагин в SMP (для сравнения) |
| Заказчик | [[10_PEOPLE/mdemyanov/mdemyanov\|Демьянов Максим]] | Фокус: «поиск информации по документации» |
| Стейкхолдер | [[10_PEOPLE/ogabdrashitova/ogabdrashitova\|Габдрашитова Ольга]] | Валидирует хотелки в SMRM |

---

## Текущий статус

**Дата обновления:** 06.06.2026
**Статус:** discovery

### Что сделано (один заход, 03.06.2026)

- ✅ Skill `naumen-docs` в `~/.claude/skills/naumen-docs/` — product-agnostic, триггерится на вопросы по SMP/Mobile/ВП/DAP.
- ✅ Crawler + chunker в `~/Knowledge/naumen-docs/scripts/`. Resumable, throttle 1.5 сек/запрос, User-Agent `naumen-docs-indexer/1.0`.
- ✅ Согласовано с владельцем доки: краулинг можно (вне зависимости от `robots.txt` — см. [[decisions/2026-06-04-respect-robots-txt|решение]]).
- ✅ Скачано: `mobile` (120 страниц) + `nsmp` (1063 страницы).
- ✅ Нарезка по H3: 224 + 1628 = **1852 чанка** с frontmatter (source_url, section, page_title, section_title, chunk_index).
- ✅ qmd-коллекция `naumen-docs`: 1852 документа, 4135 векторов, гибридный поиск (BM25 + embeddinggemma-300M + qwen3-reranker-0.6b).
- ✅ Sanity-тест: вопрос «типы атрибутов на форме мобильного приложения» → канонический чанк iOS/Android `attributes_types` со score 96%.
- ✅ Боевой тест: «типы ДПС в SMP» → канонический `action_TOC.htm` со score 90%, дословная цитата 4 типов с подтипами.
- ✅ Whitelist команд в `.claude/settings.local.json` (curl naumen, qmd, python crawl/chunk).

### В работе

- 🔄 Документация подтрека (этот index, tasks, decisions, README).

### Блокеры

- Нет.

---

## Артефакты

| Артефакт | Локация | Назначение |
|---|---|---|
| Skill | `~/.claude/skills/naumen-docs/SKILL.md` | Инструкция для Claude Code: процесс поиска, шаблон ответа, антипаттерны |
| Crawler | `~/Knowledge/naumen-docs/scripts/crawl.py` | BFS по разделу публичной доки Naumen, resumable |
| Chunker | `~/Knowledge/naumen-docs/scripts/chunk.py` | HTML → markdown с frontmatter, разрез по H3 |
| Сырой HTML | `~/Knowledge/naumen-docs/raw/{nsmp,mobile}/` | 43 МБ, кэш на случай повторного индексирования |
| Чанки | `~/Knowledge/naumen-docs/chunks/{nsmp,mobile}/` | 16 МБ markdown |
| qmd-индекс | `~/.cache/qmd/index.sqlite` (49 МБ) | BM25 + векторы |
| README | `~/Knowledge/naumen-docs/README.md` | Как запускать пайплайн |
| Логи | `~/Knowledge/naumen-docs/logs/` | crawl/chunk/embed history |

---

## Решения (decisions)

- [[decisions/2026-06-04-skill-vs-plugin|Начали со skill, плагин — позже]]
- [[decisions/2026-06-04-qmd-vs-custom-mcp|Индекс на qmd, свой MCP — когда упрёмся]]
- [[decisions/2026-06-04-respect-robots-txt|Краулинг с разрешения владельца доки, throttle 1.5 сек]]

---

## Связь с другими треками

| Трек | Связь |
|---|---|
| [[30_PROJECTS/active/ai-adoption/ask-experts/index\|ask-experts]] (родитель) | Антон+Даша делают BPM-плагин для поиска изнутри SMP. Этот подтрек — параллельная альтернатива снаружи через Claude Code. Сравнить качество на пересекающихся кейсах. |
| [[30_PROJECTS/active/ai-adoption/documentation-gramax/index\|documentation-gramax]] | Архив SMP 4.21 → markdown через инструмент Галактионова. Если/когда будет публичный markdown — можно переиспользовать для пополнения индекса qmd-search. |
| [[30_PROJECTS/active/ai-adoption/personal-effectiveness/index\|personal-effectiveness]] | Тот же класс инструмента (Claude Code skill в индивидуальном workflow). Раскатка на других аналитиков через тот же канал. |

---

## Роадмап

См. [[tasks|tasks.md]] для детальной декомпозиции.

**Discovery (сейчас):**
- Валидация качества на 10 кейсах от Даши/Антона.
- Сравнение с BPM-плагином.
- Решение: продолжаем как skill / превращаем в плагин / закрываем.

**Active (если discovery пройден):**
- Покрытие остальных разделов доки (ndap, dash, gant, service, service2, bestpractices).
- Раздать команде (минимум 2-3 аналитика).
- Расписание ежеквартального обновления индекса.

**Если будет масштаб:**
- Перейти от skill к плагину Claude Code с собственным MCP-сервером.
- Подключить внутренние источники (Confluence/портал поддержки) — отдельные коллекции qmd.
