"""Есть список заказов:
- `status` -  статус заказа
- `delivered` доставлен покупателю
- `returned` возврат
- `amount` — сумма заказа."""


def returned_sum(orders: list) -> float:
    """На какую сумму оформили возвраты."""
    return sum(order['amount'] for order in orders
               if order['status'] == 'returned')


def buyers_with_returns(orders: list) -> list:
    """Кто хотя бы раз вернул заказ."""
    buyers = []
    for order in orders:
        if order['status'] == 'returned' and order['buyer'] not in buyers:
            buyers.append(order['buyer'])
    return buyers


def count_delivered(orders: list) -> int:
    """Сколько заказов доставлено покупателю."""
    return sum(1 for order in orders if order['status'] == 'delivered')


def mean_delivered_amount(orders: list) -> float:
    """Средний чек доставленных заказов."""
    delivered_amounts = [order['amount'] for order in orders
                         if order['status'] == 'delivered']
    if not delivered_amounts:
        return 0.0
    return sum(delivered_amounts) / len(delivered_amounts)


if __name__ == '__main__':
    orders_history = [
        {'id': 1, 'buyer': 'anya', 'status': 'delivered', 'amount': 900},
        {'id': 2, 'buyer': 'boris', 'status': 'returned', 'amount': 4_500},
        {'id': 3, 'buyer': 'anya', 'status': 'delivered', 'amount': 1_500},
        {'id': 4, 'buyer': 'vera', 'status': 'delivered', 'amount': 3_200},
        {'id': 5, 'buyer': 'boris', 'status': 'delivered', 'amount': 700},
        {'id': 6, 'buyer': 'gleb', 'status': 'returned', 'amount': 2_100},
    ]

    print(f'Сколько заплатили за возвраты: {returned_sum(orders_history)}')
    print(f'Люди, возвращавшие заказы: {buyers_with_returns(orders_history)}')
    print(f'Заказов доставлено покупателю: {count_delivered(orders_history)}')
    print(f'Средний чек доставленных заказов: '
          f'{mean_delivered_amount(orders_history)}')
