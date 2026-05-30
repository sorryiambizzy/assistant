#!/usr/bin/env python3
"""
Скрипт для извлечения данных об обменниках с BestChange.
Использует requests + BeautifulSoup с улучшенным парсингом таблиц.
"""

import json
import time
import re
import traceback
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup


class BestChangeScraper:
    """Скрапер для BestChange."""

    def __init__(self):
        self.base_url = "https://www.bestchange.net"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })

    def fetch_page(self, url: str) -> str:
        """Загружает страницу и возвращает HTML."""
        print(f"Загрузка страницы: {url}")
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            text = response.text
            print(f"Страница загружена, размер: {len(text)} символов")
            return text
        except Exception as e:
            print(f"Ошибка при загрузке страницы: {e}")
            traceback.print_exc()
            return ""

    def extract_exchange_names(self, html: str) -> list[dict]:
        """Извлекает названия обменников из HTML страницы направления обмена."""
        if not html:
            return []

        try:
            soup = BeautifulSoup(html, 'html.parser')
            exchanges = []

            # Ищем ссылки на обменники (onclick атрибут или href с click.php)
            all_links = soup.find_all('a')
            print(f"Всего ссылок на странице: {len(all_links)}")

            for link in all_links:
                href = link.get('href', '')
                onclick = link.get('onclick', '')
                name = link.get_text(strip=True)

                # Ищем ссылки на обменники
                if '/click.php' in href or ('post(' in onclick or 'gotourl' in onclick):
                    if name and len(name) > 2 and len(name) < 50:
                        # Исключаем общие слова
                        exclude_words = ['обратный обмен', 'курсы обмена', 'калькулятор',
                                       'оповещение', 'двойной обмен', 'отзывы', 'faq',
                                       'помощь', 'контакты', 'мониторинг', 'обменники']
                        if name.lower() not in exclude_words:
                            if re.search(r'[a-zA-Zа-яА-ЯёЁ]', name):
                                exchanges.append({
                                    'name': name,
                                    'href': href
                                })

            # Убираем дубликаты, сохраняя порядок
            seen = set()
            unique_exchanges = []
            for ex in exchanges:
                if ex['name'] not in seen:
                    seen.add(ex['name'])
                    unique_exchanges.append(ex)

            print(f"Найдено {len(unique_exchanges)} уникальных названий обменников")

            # Выводим первые 10 для отладки
            if unique_exchanges:
                print("Примеры найденных обменников:")
                for ex in unique_exchanges[:10]:
                    print(f"  - {ex['name']}")

            return unique_exchanges

        except Exception as e:
            print(f"Ошибка при извлечении обменников: {e}")
            traceback.print_exc()
            return []

    def extract_all_exchanges_with_reserves(self, html: str) -> list[dict]:
        """Извлекает все обменники с их резервами из HTML страницы списка."""
        if not html:
            return []

        try:
            soup = BeautifulSoup(html, 'html.parser')
            exchanges = []

            # Ищем все таблицы
            tables = soup.find_all('table')
            print(f"Найдено таблиц: {len(tables)}")

            for table_idx, table in enumerate(tables):
                rows = table.find_all('tr')
                print(f"Таблица {table_idx}: {len(rows)} строк")

                # Пропускаем маленькие таблицы (вероятно, не та)
                if len(rows) < 10:
                    continue

                for row_idx, row in enumerate(rows):
                    cells = row.find_all('td')

                    # Ищем строки с достаточным количеством ячеек
                    if len(cells) >= 4:
                        # Пробуем разные варианты извлечения данных
                        # Обычно структура: [иконка, название, статус, резервы, курсы, ...]

                        # Извлекаем данные из ячеек
                        cells_text = [cell.get_text(strip=True) for cell in cells]

                        # Ищем ячейку с названием (обычно вторая)
                        name = ""
                        if len(cells) > 1:
                            name_link = cells[1].find('a')
                            if name_link:
                                name = name_link.get_text(strip=True)
                            else:
                                name = cells_text[1]

                        # Ищем статус (обычно третья)
                        status = cells_text[2] if len(cells_text) > 2 else ""

                        # Ищем резервы (обычно четвертая)
                        reserves_text = cells_text[3] if len(cells_text) > 3 else ""
                        reserves = 0

                        # Парсим резервы
                        if reserves_text:
                            # Ищем числа в тексте резервов
                            numbers = re.findall(r'[\d\s]+', reserves_text)
                            if numbers:
                                clean = ''.join(numbers).replace(' ', '')
                                try:
                                    if clean:
                                        reserves = int(clean)
                                except ValueError:
                                    pass

                        # Проверяем, что это действительно обменник
                        # Название должно быть разумной длины и не содержать общих слов
                        exclude_words = ['обменник', 'название', 'exchange', 'name', 'статус',
                                       'status', 'резервы', 'reserves', 'курс', 'rate']
                        is_valid = (
                            name and
                            2 < len(name) < 50 and
                            name.lower() not in exclude_words and
                            re.search(r'[a-zA-Zа-яА-ЯёЁ]', name) and
                            not name.isdigit() and
                            # Резервы должны быть больше 0 или текст должен содержать $
                            (reserves > 0 or '$' in reserves_text or 'USD' in reserves_text.upper())
                        )

                        if is_valid:
                            exchanges.append({
                                'name': name,
                                'status': status,
                                'reserves_raw': reserves_text,
                                'reserves_usd': reserves
                            })

            # Убираем дубликаты
            seen = set()
            unique_exchanges = []
            for ex in exchanges:
                if ex['name'] not in seen:
                    seen.add(ex['name'])
                    unique_exchanges.append(ex)

            print(f"Найдено {len(unique_exchanges)} уникальных обменников в списке")

            # Выводим первые 10 для отладки
            if unique_exchanges:
                print("Примеры найденных обменников:")
                for ex in unique_exchanges[:10]:
                    print(f"  - {ex['name']}: {ex['reserves_raw']}")

            return unique_exchanges

        except Exception as e:
            print(f"Ошибка при извлечении списка обменников: {e}")
            traceback.print_exc()
            return []

    def scrape(self) -> dict:
        """Основной метод скрапинга."""
        result = {
            'timestamp': datetime.now().isoformat(),
            'cash_exchanges': [],
            'all_exchanges': [],
            'matched': []
        }

        try:
            # Шаг 1: Извлекаем обменники с наличными
            print("\n=== Шаг 1: Извлечение обменников с наличными ===")
            cash_url = f"{self.base_url}/cash-ruble-to-bitcoin.html"
            cash_html = self.fetch_page(cash_url)
            result['cash_exchanges'] = self.extract_exchange_names(cash_html)

            # Небольшая пауза между запросами
            time.sleep(2)

            # Шаг 2: Извлекаем все обменники с резервами
            print("\n=== Шаг 2: Извлечение списка всех обменников ===")
            list_url = f"{self.base_url}/list.html"
            list_html = self.fetch_page(list_url)
            result['all_exchanges'] = self.extract_all_exchanges_with_reserves(list_html)

            # Шаг 3: Сопоставляем данные
            print("\n=== Шаг 3: Сопоставление данных ===")
            cash_names = {ex['name'].lower() for ex in result['cash_exchanges'] if ex.get('name')}

            for exchange in result['all_exchanges']:
                if exchange['name'].lower() in cash_names:
                    result['matched'].append(exchange)

            print(f"\n=== Результаты ===")
            print(f"- Обменников с наличными: {len(result['cash_exchanges'])}")
            print(f"- Всего обменников: {len(result['all_exchanges'])}")
            print(f"- Сопоставлено: {len(result['matched'])}")

            return result

        except Exception as e:
            print(f"Критическая ошибка: {e}")
            traceback.print_exc()
            return {'error': str(e)}


def main():
    """Главная функция."""
    scraper = BestChangeScraper()
    result = scraper.scrape()

    # Сохраняем результат в JSON
    output_dir = Path("/Users/epodkin/Вижуалка/executive-assistant/30_PROJECTS/active/crypto-exchanges")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Сохраняем полный результат
    json_path = output_dir / "exchanges_data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nДанные сохранены: {json_path}")

    # Создаем CSV для сопоставленных обменников
    if result.get('matched'):
        csv_path = output_dir / "cash_exchanges_reserves.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("Обменник,Статус,Резервы USD,Резервы исходный\n")
            # Сортируем по убыванию резервов
            sorted_exchanges = sorted(result['matched'], key=lambda x: x['reserves_usd'], reverse=True)
            for ex in sorted_exchanges:
                # Форматируем резервы с разделителями
                reserves_formatted = f"{ex['reserves_usd']:,}".replace(',', ' ')
                f.write(f"{ex['name']},{ex['status']},{reserves_formatted},{ex['reserves_raw']}\n")
        print(f"CSV сохранен: {csv_path}")

        # Выводим топ-10 обменников по резервам
        print("\n=== Топ-10 обменников по резервам ===")
        for i, ex in enumerate(sorted_exchanges[:10], 1):
            print(f"{i}. {ex['name']}: {ex['reserves_raw']}")

    # Также сохраняем полный список обменников
    if result.get('all_exchanges'):
        csv_path = output_dir / "all_exchanges_reserves.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("Обменник,Статус,Резервы USD,Резервы исходный\n")
            sorted_exchanges = sorted(result['all_exchanges'], key=lambda x: x['reserves_usd'], reverse=True)
            for ex in sorted_exchanges:
                reserves_formatted = f"{ex['reserves_usd']:,}".replace(',', ' ')
                f.write(f"{ex['name']},{ex['status']},{reserves_formatted},{ex['reserves_raw']}\n")
        print(f"Полный список сохранен: {csv_path}")

    return result


if __name__ == "__main__":
    main()
