import os
from datetime import datetime

PATH = 'log.txt'


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            nonlocal path
            with open(path, 'a', encoding='utf-8') as file:
                file.write(
                    f"[{datetime.now()}] func_name: {old_function.__name__}, args: {args}, kwargs: {kwargs}, result: {result}\n")
            return result
        return new_function
    return __logger


class CookBook:
    @logger(PATH)
    def __init__(self):
        self.full_book = self.read_file('dishes.txt')

    @logger(PATH)
    def get_shop_list_by_dishes(self, dishes, person_count):
        result = {}
        for dish in dishes:
            if dish not in self.full_book:
                print(f'Блюда "{dish}" нет в кулинарной книге.')
                continue
            for ingredient in self.full_book[dish]:
                if ingredient['ingredient_name'] in result:
                    result[ingredient['ingredient_name']]['quantity'] += ingredient['quantity'] * person_count
                else:
                    result[ingredient['ingredient_name']] = {'measure': ingredient['measure'],
                                                             'quantity': ingredient['quantity'] * person_count}
        return result

    @logger(PATH)
    def read_file(self, file_name):
        result = {}
        with open(file_name, encoding='utf-8') as file:
            while line := file.readline():
                dish_name = line.strip()
                ingredients_count = int(file.readline())
                ingredients = []
                for i in range(ingredients_count):
                    name, count, measure = file.readline().strip().split(' | ')
                    ingredients.append({'ingredient_name': name, 'quantity': int(count), 'measure': measure})
                result[dish_name] = ingredients
                file.readline()
        return result


@logger(PATH)
def main():
    cook_book = CookBook()
    print(cook_book.full_book)
    print(cook_book.get_shop_list_by_dishes(['Фахитос', 'Омлет'], 2))


if __name__ == '__main__':
    main()