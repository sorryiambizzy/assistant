# Справочник qmd

## Установка

```bash
npm install -g @tobilu/qmd
```

## MCP-инструменты

| Инструмент | Описание |
|------------|----------|
| `qmd_deep_search` | Гибридный поиск с reranking (основной) |
| `qmd_search` | Точный поиск BM25 по слову, ID, frontmatter |
| `qmd_vector_search` | Семантический поиск без reranking |
| `qmd_get` | Получить документ по пути |
| `qmd_multi_get` | Получить несколько документов по паттерну |
| `qmd_status` | Диагностика индекса и коллекций |

## CLI-команды

```bash
qmd collection add ./path --name name --mask "*.md"  # Создать коллекцию
qmd collection list                                     # Список коллекций
qmd update                                              # Переиндексация
qmd embed                                               # Создать эмбеддинги
qmd query "запрос"                                      # Поиск с reranking
qmd search "запрос"                                     # BM25 поиск
qmd mcp                                                 # Запустить MCP-сервер
```

## Опции поиска

- `-n <num>` — количество результатов (по умолчанию 5)
- `-c <collection>` — фильтр по коллекции
- `--full` — полный документ вместо сниппета
- `--files` — вывод docid,score,filepath

## Золотое правило

Поиск по ID (`amuratov`) работает 100%. По русским именам — используй `qmd_deep_search`.

## Если qmd не установлен

Используй встроенные инструменты Claude Code:
- `Grep` — поиск по содержимому файлов
- `Glob` — поиск файлов по паттерну
- `Read` — чтение файла
