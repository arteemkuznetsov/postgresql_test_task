import random
import string
import json
import os
import csv
import shutil


def main():
    categories = generate_rand_categories(1000, 8)
    json = read_json('./in/config.json')
    if json:
        write_out_tables(json, categories)
    else:
        print('Config error!')


def generate_rand_categories(arr_len, str_len):
    categories = []
    for i in range(0, arr_len):
        categories.append(
            ''.join(random.choices(string.ascii_letters, k=str_len))
        )

    return categories


def read_json(path):
    try:
        with open(path) as file:
            return json.load(file)
    except IOError:
        return None


def write_csv(data, path):
    with open(path, 'w', newline='') as csvfile:
        header = ['category', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def generate_csv(categories):
    rows = []
    # рандомное количество строк - категорий
    for i in range(1, random.randint(1, len(categories)) + 1):
        rows.append({'category': categories[i], 'count': 1})
    return rows


def create_empty_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def write_out_tables(json, categories):
    out_path = './out'
    create_empty_dir(out_path)

    for value in json:
        parent_path = f"{out_path}/{value['location']}/{value['source']}"
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
            for date in value['dates']:
                child_path = f"{parent_path}/{date}"
                if not os.path.exists(child_path):
                    os.mkdir(child_path)

                    # рандомное количество таблиц от 1 до 5 включительно
                    for i in range(1, random.randint(1, 6)):
                        random.shuffle(categories)
                        write_csv(
                            generate_csv(categories),
                            f"{child_path}/table_{i}.csv"
                        )
