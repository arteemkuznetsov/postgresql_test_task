import random
import json
import os
import csv
import shutil


def main():
    """Точка входа"""
    print('generating tables started')
    categories = read_categories('./categories.csv')
    json_file = read_json('./in/config.json')
    if json_file:
        write_out_tables(json_file, categories)
    else:
        print('Config error!')
    print('generating tables finished')


def read_categories(path: str) -> list | None:
    """
    Читает csv-файл со списком сгенерированных категорий
    :param path: путь к файлу
    :return: список словарей или None
    """
    try:
        with open(path, newline='') as csvfile:
            return [x[0] for x in csv.reader(csvfile)]
    except IOError:
        return None


def read_json(path: str) -> list | None:
    """
    Читает json-файл
    :param path: путь к json-файлу
    :return: список словарей или None
    """
    try:
        with open(path) as file:
            return json.load(file)
    except IOError:
        return None


def write_csv(data: list, path: str):
    """
    Записывает csv-файл с полями category, count
    :param data: список данных в формате {category, count}
    :param path: путь к файлу
    """
    with open(path, 'w', newline='') as csvfile:
        header = ['category', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def generate_csv(categories: list) -> list:
    """
    Генерирует csv-файл в формате {category, count}
    :param categories: список категорий
    :return: список в формате csv-файла
    """
    rows = []
    for i in range(0, random.randint(1, len(categories))):
        rows.append({'category': categories[i], 'count': 1})
    return rows


def create_empty_dir(path: str):
    """
    Создает пустую директорию, перезаписывая существующую
    :param path: путь к директории
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def create_tables_in_dir(categories: list, path: str):
    """
    Создает директорию с учетом вложенности и наполняет ее сгенерированными csv-таблицами
    :param categories: список категорий
    :param path: путь к директории
    """
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(1, random.randint(1, 6)):
        random.shuffle(categories)
        write_csv(
            generate_csv(categories),
            f"{path}/table_{i}.csv"
        )


def write_out_tables(json_file: list, categories: list):
    """
    Обходит значения во входном json-файле, обходит даты в значениях, для каждой даты вызывает create_tables_in_dir
    :param json_file: прочитанный json-файл
    :param categories: список категорий
    """
    out_path = './out'
    create_empty_dir(out_path)

    for value in json_file:
        for date in value['dates']:
            create_tables_in_dir(
                categories,
                f"{out_path}/{value['location']}/{value['source']}/{date}"
            )


if __name__ == "__main__":
    main()
