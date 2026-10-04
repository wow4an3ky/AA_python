"""Дана история поисковых запросов: каждая строка — один введённый запрос.
Повтор в списке значит, что этот запрос ввели ещё раз."""


def total_queries(queries: list) -> int:
    """Сколько всего поисковых запросов в ленте."""
    return len(queries)


def count_query_frequencies(queries: list) -> dict:
    """Сколько раз ввели каждый запрос."""
    frequency = {}
    for query in queries:
        frequency[query] = frequency.get(query, 0) + 1
    return frequency


def most_frequent_query(frequency: dict) -> str:
    """Какой запрос вводили чаще всего."""
    return max(frequency, key=frequency.get)


def most_frequent_query_share(frequency: dict, queries: list) -> float:
    """Какую долю всех поисков занимает самый частый запрос."""
    return frequency[most_frequent_query(frequency)] / len(queries)


def queries_seen_once(frequency: dict) -> list:
    """Какие запросы встретились один раз."""
    return [query for query in frequency if frequency.get(query) == 1]


if __name__ == '__main__':
    queries_history = [
        'чехол',
        'iphone',
        'чехол',
        'наушники',
        'iphone',
        'iphone',
        'кабель',
        'чехол',
        'iphone',
    ]

    query_frequencies = count_query_frequencies(queries_history)

    print(f'Всего поисковых запросов в ленте: '
          f'{total_queries(queries_history)}')
    print(f'Частоты каждого из запросов: {query_frequencies}')
    print(f'Самый частый запрос: {most_frequent_query(query_frequencies)}')
    print(f'Доля самого частого запроса среди всех: '
          f'{most_frequent_query_share(query_frequencies, queries_history)}')
    print(f'Один раз встретились: {queries_seen_once(query_frequencies)}')
