---
type: project
id: "ncc"
title: "NCC"
status: active
project_type: umbrella
priority: high
owner: "epodkin"
start_date: 2026-03-31
target_date: ""
domain: technology
tags:
  - project
  - umbrella
  - ncc
---

# NCC

**ID:** `= this.id`
**Статус:** `= this.status`
**Приоритет:** `= this.priority`
**Владелец:** `= this.owner`

> Зонтичный проект NCC объединяет два направления для одного и того же клиентского контура: переписывание чат-SDK и встроенную в приложение VoIP-звонилку.

---

## Подпроекты

| Проект | Цель | Статус |
|--------|------|--------|
| [[30_PROJECTS/active/ncc/sdk-2/sdk-2\|Chat SDK 2.0]] | Переписать Chat SDK с устранением легаси, под клиента Магнит | active |
| [[30_PROJECTS/active/ncc/voip/voip\|VoIP звонилка]] | Встроенная в приложение звонилка на WebRTC (замена PJSIP) | planning |

---

## Общий контекст

- **Заказчик:** Магнит (через А. Гусева и А. Ликулина), потенциально другие клиенты по запросу звонилки.
- **Команда:** общая по обоим направлениям ([[10_PEOPLE/iportnov/iportnov|Иван Портнов]] — техлид/Android, [[10_PEOPLE/sprokopiev/sprokopiev|Сергей Прокопьев]] — iOS).
- **Менеджерские задачи** ведутся в одном месте — [[30_PROJECTS/active/ncc/management-tasks|management-tasks.md]] (секции SDK 2.0 и Звонилка).
- **Ресурсный план Q3 2026:** [[30_PROJECTS/active/ncc/team-load-jun-aug-2026|team-load-jun-aug-2026.md]] (распределение нагрузки между SDK 2.0 и звонилкой).

---

## Зависимости между направлениями

- Старт активной разработки звонилки — после стабилизации релиза SDK 2.0 на iOS (~29.06) и публикации Android.
- Олег + Артём стабилизируют SDK и публикуют его, остальная команда переходит на звонилку.
- Синхронизация отпусков команд устроена так, чтобы минимизировать простой обоих направлений.

---

## Связанные материалы

- [[10_PEOPLE/epodkin/epodkin|Подкин Евгений]] — владелец
- [[10_PEOPLE/iportnov/iportnov|Иван Портнов]] — техлид
- [[10_PEOPLE/sprokopiev/sprokopiev|Сергей Прокопьев]] — iOS-лид
- [[40_DECISIONS/records/DEC-0001|DEC-0001]] — решения по NCC
