"""Оформление вариантов отчетов по сотрудникам:
1. Иерархия: для каждого департамента показать,
какие команды в него входят.
2. Сводка по департаментам: название, сколько человек,
минимальная и максимальная зарплата, средняя по каждому департаменту.
3. То же самое, что в "2", но записанное в csv-файл.
Имя выходного файла можно захардкодить(например, константой в начале файла)
или передавать опциональным параметром в эту же функцию."""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / 'Corp_Summary.csv'
OUTPUT_FILE = BASE_DIR / 'departmental_summary.csv'


def import_csv(path: str) -> list[list[str]]:
    '''Импортируем csv файл.'''
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        return list(reader)


def hierarchy(data: list[list[str]]) -> dict[str, set[str]]:
    '''Показывает для каждого департамента какие команды в него входят.'''
    department_teams = {}
    for person in data:
        department_teams.setdefault(person[1], set()).add(person[2])
    return department_teams


def departmental_summary(data: list[list[str]]) -> dict[str, dict]:
    '''Сводка по департаментам (название + статистика).'''
    people_in_department = {}
    department_statistics = {}
    for person in data:
        people_in_department.setdefault(
            person[1], []
        ).append(int(person[5]))
    for department, stats in people_in_department.items():
        department_statistics[department] = {
            'number_of_employees': len(stats),
            'minimum_salary': min(stats),
            'maximum_salary': max(stats),
            'average_salary': (
                sum(stats) / len(stats))
        }
    return department_statistics


def save_departmental_summary_csv(
        data: list[list[str]], output_file: str
) -> None:
    '''Запись сводки по департаментам в csv файл.'''
    department_statistics = departmental_summary(data)
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer= csv.writer(f, delimiter=';')
        writer.writerow([
            'department',
            'number_of_employees',
            'minimum_salary',
            'maximum_salary',
            'average_salary',
        ])
        for department, stats in department_statistics.items():
            writer.writerow([
                department,
                stats['number_of_employees'],
                stats['minimum_salary'],
                stats['maximum_salary'],
                stats['average_salary'],
            ])


def print_hierarchy(department_teams: dict[str, set[str]]) -> None:
    '''Вывод на экран отчета - иерархии.'''
    for department, teams in department_teams.items():
        print(f'Департамент {department} включает команды: {sorted(teams)}')


def print_departmental_summary(department_statistics: dict[str, dict]) -> None:
    '''Вывод на экран сводок по департаментам.'''
    for department, stats in department_statistics.items():
        print(f'Сводка по департаменту {department}: ')
        print(
            f'Количество людей в департаменте: '
            f'{stats["number_of_employees"]}'
        )
        print(
            f'Минимальная зарплата в департаменте: '
            f'{stats["minimum_salary"]}'
        )
        print(
            f'Максимальная зарплата в департаменте: '
            f'{stats["maximum_salary"]}'
        )
        print(
            f'Средняя зарплата в департаменте: '
            f'{stats["average_salary"]}\n'
        )


def main(option: int, input_path: str, output_path: str) -> None:
    '''Оформление отчета в зависимости от варианта.'''
    imported_csv = import_csv(input_path)
    if option == 1:
        print_hierarchy(hierarchy(imported_csv))
    elif option == 2:
        print_departmental_summary(departmental_summary
                                   (imported_csv))
    elif option == 3:
        save_departmental_summary_csv(imported_csv, output_path)
        print(f'Сохранено по пути: {output_path}')
    else:
        print('Ошибка значения')


if __name__ == '__main__':
    command = int(input())
    main(command, INPUT_PATH, OUTPUT_FILE)