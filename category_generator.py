import csv
import random
import string


def main():
    """Точка входа"""
    print('generating categories started')
    categories = generate_rand_categories(1000, 8)
    write_categories_to_file(categories, './categories.csv')
    print('generating categories finished')


def generate_rand_categories(arr_len: int, str_len: int) -> list:
    """
    Генерирует рандомное количество рандомных строк-категорий
    :param arr_len: максимальное количество строк
    :param str_len: длина строки
    :return: список сгенерированных строк
    """
    categories = []
    for i in range(1, arr_len + 1):
        categories.append(''.join(random.choices(string.ascii_letters, k=str_len)))

    return categories


def write_categories_to_file(data: list, path: str):
    """
    Записывает список сгенерированных строк-категорий в csv-файл
    :param data: список строк
    :param path: путь к файлу
    """
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow((row,))


if __name__ == "__main__":
    main()
