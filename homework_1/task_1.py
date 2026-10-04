"""Один и тот же товар может лежать на складе в Москве, в Казани или в обоих
городах. Ниже id товаров на каждом складе."""


def goods_in_both_cities(moscow: set, kazan: set) -> set:
    """Что можно забрать в обоих городах."""
    return moscow & kazan


def goods_only_in_moscow(moscow: set, kazan: set) -> set:
    """Что есть только в Москве."""
    return moscow - kazan


def goods_only_in_kazan(moscow: set, kazan: set) -> set:
    """Что есть только в Казани."""
    return kazan - moscow


def unique_goods_at_both_cities(moscow: set, kazan: set) -> int:
    """Сколько разных товаров на обоих складах вместе."""
    return len(moscow | kazan)


if __name__ == '__main__':
    moscow_goods = {201, 202, 203, 204}
    kazan_goods = {203, 204, 205, 206}

    print(f'В обоих городах можно забрать: '
          f'{goods_in_both_cities(moscow_goods, kazan_goods)}')
    print(f'Только в Москве есть: '
          f'{goods_only_in_moscow(moscow_goods, kazan_goods)}')
    print(f'Только в Казани есть: '
          f'{goods_only_in_kazan(moscow_goods, kazan_goods)}')
    print(f'Уникальных товаров на обоих складах вместе: '
          f'{unique_goods_at_both_cities(moscow_goods, kazan_goods)}')
