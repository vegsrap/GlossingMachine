def morph(glossed):
    """
    Определяет тип морфологической структуры.
    Возвращает кортеж (тип, альтернатива_есть)
    тип: 'Isolating', 'Polysynthetic', 'Agglutinative', 'Fusional'
    альтернатива_есть: True/False
    """
    words = glossed.split()
    if not words:
        return ('Не определено', False)

    total_words = len(words)

    # Стоп-слова (теги частей речи)
    tag_stopwords = {'V', 'N', 'PRO', 'ADJ', 'ADV', 'PRON', 'DET', 'CONJ', 'PREP', 'ADP', 'PART', 'AUX', 'NUM'}

    # Собираем информацию
    all_morphemes = []
    lexical_morphemes = []  # корни/основы (первая морфема в слове)
    grammatical_morphemes = []  # грамматические показатели

    for word in words:
        morphemes = word.split('-')

        # Первая морфема — обычно лексическая (корень)
        if morphemes:
            root = morphemes[0]
            # Проверяем, не тег ли это
            if root.upper() not in tag_stopwords and not (len(root) == 1 and root.isalpha()):
                lexical_morphemes.append(root)
                all_morphemes.append(root)

        # Остальные морфемы — потенциально грамматические
        for m in morphemes[1:]:
            m_upper = m.upper()
            if m_upper not in tag_stopwords and not (len(m) == 1 and m.isalpha() and m_upper in 'VNAD'):
                all_morphemes.append(m)
                # Проверяем, похоже ли на грамматический маркер
                if any(cat in m_upper for cat in ['ERG', 'ABS', 'NOM', 'ACC', 'DAT', 'GEN', 'LOC',
                                                  'PST', 'FUT', 'PRS', 'PL', 'SG', '1', '2', '3']):
                    grammatical_morphemes.append(m)

    if not all_morphemes:
        return ('Не определено', False)

    # 1. Индекс синтетичности
    synthetic_index = len(all_morphemes) / total_words

    # 2. Соотношение грамматических и лексических морфем
    gram_ratio = len(grammatical_morphemes) / len(all_morphemes) if all_morphemes else 0

    # 3. Уникальность морфем (в фузионных языках меньше уникальных морфем)
    unique_morphemes = set(all_morphemes)
    uniqueness_ratio = len(unique_morphemes) / len(all_morphemes) if all_morphemes else 1

    # 4. Составные глоссы с точками
    dot_count = glossed.count('.')

    # 5. Средняя длина морфемы (в символах) — короткие морфемы признак фузии
    avg_morph_length = sum(len(m) for m in all_morphemes) / len(all_morphemes)

    # 6. Наличие маркеров, которые обычно бывают фузионными
    fusional_hints = 0
    fusional_markers = {'1SG', '2SG', '3SG', '1PL', '2PL', '3PL',  # лично-числовые
                        'PST', 'FUT', 'PRS',  # временные
                        'PFV', 'IPFV', 'IMPF', 'PERF'}  # видовые

    for m in grammatical_morphemes:
        m_upper = m.upper()
        # Если одна морфема содержит признаки нескольких категорий
        if m_upper in fusional_markers:
            fusional_hints += 1
        # Если морфема длинная (3+ символов) и не похожа на агглютинативный маркер
        if len(m) >= 3 and m_upper not in ['ERG', 'ABS', 'NOM', 'ACC', 'DAT', 'GEN', 'LOC']:
            fusional_hints += 0.5

    # 7. Определение типа
    # Изолирующий язык
    if synthetic_index < 1.15:
        return ('Isolating', False)

    # Полисинтетический язык
    if synthetic_index > 2.4:
        return ('Polysynthetic', False)

    # Фузионный язык (уверенно)
    if fusional_hints > 2 or dot_count > 0:
        return ('Fusional', True)  # фузионный, но возможен агглютинативный

        # 4. Неоднозначная зона: синтетический индекс 1.15–2.4
    if synthetic_index >= 1.15:
            return ('Agglutinative', True)  # агглютинативный, но возможен фузионный

    return ('Не определено', False)

