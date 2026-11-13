"""Векторизаторы текста и получение важных слов
при помощи следующих классов:
- CountVectorizer: частоты токенов
- BinaryVectorizer: наличие токенов
- TfidfVectorizer: веса TF-IDF
- KeywordExtractor: лучшие n слов по весам токенизаторов. 
"""


import math


TRAIN_CORPUS = [
    'Марс сигнал сигнал',
    'Марс пыль',
    'Марс сигнал антенна',
]
CHECK_CORPUS = [
    'СИГНАЛ шум сигнал',
    'антенна пыль',
    'марс марс марс',
    'комета',
    ' ',
]


class CountVectorizer:
    """Превращает текст в набор чисел."""

    def __init__(self, lowercase: bool = True, ngram_size: int = 1) -> None:
        """Инициализация начального состояния."""
        self.vocabulary = {}
        self.lowercase = lowercase
        self.ngram_size = ngram_size

    def add_word(self, word: str) -> int:
        """Добавляем новое слово в словарь и возвращаем индекс."""
        if word in self.vocabulary:
            return self.vocabulary[word]
        new_index = len(self.vocabulary)
        self.vocabulary[word] = new_index
        return new_index

    def tokenize(self, text: str) -> list[str]:
        """Токенизация текста с учетом размера ngram."""
        if self.lowercase:
            text = text.lower()

        words = text.split()
        if len(words) < self.ngram_size:
            return []
        if self.ngram_size == 1:
            return words
        tokenized_text = []
        for i in range(len(words) - self.ngram_size + 1):
            ngram = ' '.join(words[i:i+self.ngram_size])
            tokenized_text.append(ngram)
        return tokenized_text

    def fit(self, corpus: list[str]) -> None:
        """Создание словаря индексированных токенов."""
        pre_vocabulary = {}

        for text in corpus:
            tokens = self.tokenize(text)
            for token in tokens:
                if token not in pre_vocabulary:
                    pre_vocabulary[token] = len(pre_vocabulary)

        if not pre_vocabulary:
            raise ValueError('Нет токенов')
        self.vocabulary = pre_vocabulary

    def transform(self, corpus: list[str]) -> list[list[int]]:
        """Создание матрицы частот."""
        if len(self.vocabulary) == 0:
            raise RuntimeError('Модель не обучена')
        freqs = []
        for text in corpus:
            vector = [0] * len(self.vocabulary)
            tokens = self.tokenize(text)
            for token in tokens:
                if token in self.vocabulary:
                    ind = self.vocabulary[token]
                    if ind < len(vector):
                        vector[ind] += 1
            freqs.append(vector)
        return freqs

    def get_feature_names(self) -> list[str]:
        """Названия признаков из словаря в порядке индексов."""
        pairs = sorted(self.vocabulary.items(), key=lambda x: x[1])
        return [word[0] for word in pairs]

    def fit_transform(self, corpus: list[str]) -> list[list[int]]:
        """Создание словаря токенов и матрицы частот."""
        self.fit(corpus)
        return self.transform(corpus)

    def __delattr__(self, name: str) -> None:
        """Сбрасывает словарь."""
        if name == 'vocabulary':
            self.vocabulary = {}
        else:
            super().__delattr__(name)

    def to_dict(self) -> dict:
        """Сохранение текущей модели."""
        return {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self.vocabulary.copy()
        }

    @classmethod
    def from_dict(cls, state: dict) -> 'CountVectorizer':
        """Создание готового экземпляра класса."""
        new_obj = cls(
            lowercase=state['lowercase'],
            ngram_size=state['ngram_size']
        )
        new_obj.vocabulary = state['vocabulary'].copy()
        return new_obj


class BinaryVectorizer(CountVectorizer):
    """Превращает текст в набор бинарных чисел."""

    def transform(self, corpus: list[str]) -> list[list[int]]:
        """Создание матрицы появления."""
        if len(self.vocabulary) == 0:
            raise RuntimeError('Модель не обучена')
        freqs = []
        for text in corpus:
            vector = [0] * len(self.vocabulary)
            tokens = self.tokenize(text)
            for token in tokens:
                if token in self.vocabulary:
                    ind = self.vocabulary[token]
                    if ind < len(vector):
                        vector[ind] = 1
            freqs.append(vector)
        return freqs


class TfidfVectorizer(CountVectorizer):
    """Выделение важных слов текста."""

    def __init__(
        self,
        lowercase: bool = True,
        ngram_size: int = 1,
        use_idf: bool = True
    ) -> None:
        """Инициализация начального состояния."""
        super().__init__(lowercase=lowercase, ngram_size=ngram_size)
        self.use_idf = use_idf
        self._idf = []

    def fit(self, corpus: list[str]) -> 'TfidfVectorizer':
        """Строит словарь и IDF."""
        super().fit(corpus)
        if not self.use_idf:
            self._idf = []
            return self
        n = len(corpus)
        df = {token: 0 for token in self.vocabulary}
        for text in corpus:
            for token in set(self.tokenize(text)):
                if token in df:
                    df[token] += 1
        self._idf = [
            math.log((n + 1) / (df[token] + 1)) + 1
            for token in self.get_feature_names()
        ]
        return self

    def transform(self, corpus: list[str]) -> list[list[float]]:
        """Матрица TF-IDF."""
        if len(self.vocabulary) == 0:
            raise RuntimeError('Модель не обучена')
        freqs = super().transform(corpus)
        tf_idf = []

        for row in freqs:
            known = sum(row)
            if known == 0:
                tf_idf.append([0.] * len(row))
            elif self.use_idf:
                tf_idf.append([
                    (count / known) * idf_val
                    for count, idf_val in zip(row, self._idf)
                ])
            else:
                tf_idf.append([count / known for count in row])
        return tf_idf

    @classmethod
    def from_config(cls, config: dict) -> 'TfidfVectorizer':
        """Создание готового экземпляра класса."""
        return cls(
            lowercase=config.get('lowercase', True),
            use_idf=config.get('use_idf', True)
        )

    @property
    def idf(self) -> list[float]:
        """Список весов по порядку без влияния изменений."""
        return self._idf.copy()


class KeywordExtractor:
    """Храним векторизатор и выбираем ключевые слова по весам."""

    def __init__(self, vectorizer, top_n: int = 3) -> None:
        """Инициализация начального состояния."""
        self.vectorizer = vectorizer
        self.top_n = top_n

    @property
    def top_n(self) -> int:
        """Максимальное число слов на один текст."""
        return self._top_n

    @top_n.setter
    def top_n(self, value: int) -> None:
        """Проверка top_n на тип данных и знак."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError('top_n должен быть int > 0.')
        self._top_n = value

    def fit(self, corpus: list[str]) -> 'KeywordExtractor':
        """Обучение векторизатора на корпусе."""
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus: list[str]) -> list[list[tuple[str, float]]]:
        """Возвращает список пар (слово, вес) для каждого текста."""
        weights_matrix = self.vectorizer.transform(corpus)
        feature_names = self.vectorizer.get_feature_names()
        pairs_list = []

        for row in weights_matrix:
            text_pairs = []
            for i, weight in enumerate(row):
                if weight > 0:
                    text_pairs.append((feature_names[i], weight))
            text_pairs.sort(key=lambda pair: (-pair[1], pair[0]))
            pairs_list.append(text_pairs[:self.top_n])
        return pairs_list


def demo() -> None:
    """Выполняется один из трех сценариев."""

    print('Сценарий 1: Веса TF-IDF')
    tfidf = TfidfVectorizer.from_config({})
    matrix = tfidf.fit_transform(TRAIN_CORPUS)

    print(f'Слова: {tfidf.get_feature_names()}')
    print(f'IDF: {tfidf.idf}')
    for text, row in zip(TRAIN_CORPUS, matrix):
        print(f'{text}: {row}')

    idf_copy = tfidf.idf
    idf_copy.clear()
    print(f'IDF после очистки: {tfidf.idf}')

    print('\nСценарий 2: Настройки и новый fit()')
    tf = TfidfVectorizer.from_config({'lowercase': False, 'use_idf': False})
    texts = ['Марс марс', 'МАРС сигнал']

    tf.fit(texts)
    print(f'Слова: {tf.get_feature_names()}')
    print(f'IDF: {tf.idf}')
    print('TF:')
    for text, row in zip(texts, tf.transform(texts)):
        print(f'{text}: {row}')

    tfidf.fit(['Венера облака'])
    print(f'Слова: {tfidf.get_feature_names()}')
    print(f'IDF: {tfidf.idf}')
    print('Матрица для строки -Марс Венера облака-: ')
    for row in tfidf.transform(['Марс Венера облака']):
        print(row)

    print('\nСценарий 3: Ключевые слова')
    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(TRAIN_CORPUS)

    print('При top_n = 2: ')
    for text, pairs in zip(CHECK_CORPUS, extractor.extract(CHECK_CORPUS)):
        print(f'{text}: {pairs}')

    extractor.top_n = 1
    print('При top_n = 1: ')
    for text, pairs in zip(CHECK_CORPUS, extractor.extract(CHECK_CORPUS)):
        print(f'{text}: {pairs}')

    print()
    try:
        extractor.top_n = 0
    except ValueError as error:
        print(f'ValueError при top_n = 0: {error}')


if __name__ == '__main__':
    demo()
