import random
import string
import json
import os
import csv
import shutil


def main():
    """Точка входа"""
    categories = generate_rand_categories(1000, 8)
    json_file = read_json('./in/config.json')
    if json_file:
        write_out_tables(json_file, categories)
    else:
        print('Config error!')


def generate_rand_categories(arr_len, str_len) -> list:
    """
    Генерирует рандомное количество рандомных строк категорий
    :param arr_len: максимальное количество категорий
    :param str_len: длина строки категории
    :return: список строк категорий
    """
    categories = []
    for i in range(1, arr_len + 1):
        categories.append(
            ''.join(random.choices(string.ascii_letters, k=str_len))
        )

    return categories


def read_json(path) -> list | None:
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


def write_csv(data, path):
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


def generate_csv(categories) -> list:
    """
    Генерирует csv-файл в формате {category, count}
    :param categories: список категорий
    :return: список в формате csv-файла
    """
    rows = []
    for i in range(0, random.randint(1, len(categories))):
        rows.append({'category': categories[i], 'count': 1})
    return rows


def create_empty_dir(path):
    """
    Создает пустую директорию, перезаписывая существующую
    :param path: путь к директории
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def create_tables_in_dir(categories, path):
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


def write_out_tables(json_file, categories):
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


main()
