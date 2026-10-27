"""Есть список отзывов на товары. На каждой строке — по одному.
Данные слегка битые, и названия товара записаны в разном регистре.
`id` при этом один и тот же для одного и того же товара.
Перед подсчётом приведите названия к одному формату,
иначе они будут считаться как разные."""


def ratings_each_products(reviews: list) -> dict:
    """Все оценки для каждого товара."""
    products_ratings = {}
    for review in reviews:
        product = review['product']
        products_ratings.setdefault(product, []).append(review['stars'])
    return products_ratings


def avg_rating_each_products(products_ratings: dict) -> dict:
    """Средняя оценка каждого товара."""
    return {product: sum(ratings) / len(ratings)
            for product, ratings in products_ratings.items()}


def lowest_avg_rating_with_enough_reviews(products_ratings: dict) -> str:
    """Худший товар по средней оценке среди тех,
    у кого хотя бы два отзыва."""
    products_rating_with_enough_reviews = {product: sum(ratings) / len(ratings)
                                           for product, ratings
                                           in products_ratings.items()
                                           if len(ratings) >= 2}
    if not products_rating_with_enough_reviews:
        return ''
    return min(products_rating_with_enough_reviews,
               key=products_rating_with_enough_reviews.get)


def reviews_with_two_or_fewer_stars(reviews: list) -> int:
    """Сколько отзывов на 1 или 2 звезды."""
    return sum(1 for review in reviews if review['stars'] in [1, 2])


def overall_share_of_negative_reviews(count_bad_reviews: int,
                                      reviews: list) -> float:
    """Какую долю всех отзывов составляют плохие."""
    if not reviews:
        return 0.0
    return count_bad_reviews / len(reviews)


if __name__ == '__main__':
    reviews_history = [
        {'id': 1, 'product': 'Чехол', 'stars': 5},
        {'id': 1, 'product': 'Чехол', 'stars': 3},
        {'id': 1, 'product': 'Чехол', 'stars': 4},
        {'id': 2, 'product': 'Наушники', 'stars': 2},
        {'id': 2, 'product': 'наушники', 'stars': 2},
        {'id': 2, 'product': 'НАУШНИКИ', 'stars': 5},
        {'id': 3, 'product': 'Планшет', 'stars': 5},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 4, 'product': 'Колонка', 'stars': 4},
        {'id': 5, 'product': 'Кабель', 'stars': 1},
    ]

    for product_review in reviews_history:
        product_review['product'] = product_review['product'].capitalize()

    counter_bad_reviews = reviews_with_two_or_fewer_stars(reviews_history)
    all_products_ratings = ratings_each_products(reviews_history)
    share = overall_share_of_negative_reviews(counter_bad_reviews,
                                              reviews_history)

    print(f'Средняя оценка каждого товара: '
          f'{avg_rating_each_products(all_products_ratings)}')
    print(f'Худший товар по средней оценке среди тех, '
          f'у кого есть хотя бы 2 отзыва: '
          f'{lowest_avg_rating_with_enough_reviews(all_products_ratings)}')
    print(f'Отзывов на 1 или 2 звезды: '
          f'{counter_bad_reviews}')
    print(f'Доля плохих отзывов среди всех: {share}')
