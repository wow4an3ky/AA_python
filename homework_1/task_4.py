"""Есть статистика за пять дней работы магазина.
У каждого дня число заказов, выручка и число возвратов."""


def weekly_revenue(days: list) -> float:
    """Выручка за всю неделю."""
    return sum(day['revenue'] for day in days)


def max_revenue_day(days: list) -> str:
    """День с самой большой выручкой."""
    revenue_by_day = {day['day']: day['revenue'] for day in days}
    return max(revenue_by_day, key=revenue_by_day.get)


def mean_revenue_per_order(days: list) -> dict:
    """Средняя выручка на один заказ каждый день."""
    revenue_per_order = {}
    for day in days:
        if day['orders'] != 0:
            revenue_per_order[day['day']] = day['revenue'] / day['orders']
        else:
            revenue_per_order[day['day']] = 0.0
    return revenue_per_order


def days_with_returns_over_20_percent(days: list) -> list:
    """Дни, где возвратов больше 20% заказов."""
    threshold = 0.2
    days_with_over_threshold = []
    for day in days:
        if day['orders'] != 0 and (day['returns'] / day['orders']) > threshold:
            days_with_over_threshold.append(day['day'])
    return days_with_over_threshold


if __name__ == '__main__':
    working_days = [
        {'day': 'пн', 'orders': 20, 'revenue': 40_000, 'returns': 2},
        {'day': 'вт', 'orders': 16, 'revenue': 19_200, 'returns': 4},
        {'day': 'ср', 'orders': 25, 'revenue': 55_000, 'returns': 1},
        {'day': 'чт', 'orders': 10, 'revenue': 12_000, 'returns': 3},
        {'day': 'пт', 'orders': 30, 'revenue': 48_000, 'returns': 3},
    ]

    print(f'Недельная выручка: {weekly_revenue(working_days)}')
    print(f'Самая большая выручка в: {max_revenue_day(working_days)}')
    print(f'Средняя выручка за один заказ каждый день: '
          f'{mean_revenue_per_order(working_days)}')
    print(f'Возвратов больше 20% в: '
          f'{days_with_returns_over_20_percent(working_days)}')
