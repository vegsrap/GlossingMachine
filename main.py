def param_label(value: str) -> str:
    if value == 'Unknown':
        return 'не удалось распознать'
    return value


def alignment(glossed):
    s = []
    for i in glossed.split():
        parts = i.split('-')
        s.extend(parts)

    erg_count = s.count("ERG")
    abs_count = s.count("ABS")
    nom_count = s.count("NOM")
    acc_count = s.count("ACC")

    erg_score = erg_count + abs_count
    acc_score = nom_count + acc_count
    total = erg_score + acc_score

    if total < 2:
        return "Не определено"

    erg_ratio = erg_score / total
    acc_ratio = acc_score / total

    if erg_ratio >= 0.2 and acc_ratio >= 0.2:
        return f"Расщеплённая эргативность (эрг: {erg_ratio:.0%}, акк: {acc_ratio:.0%})"
    if erg_ratio > acc_ratio:
        return f"Эргативная ({erg_ratio:.0%} маркеров)"
    elif acc_ratio > erg_ratio:
        return f"Аккузативная ({acc_ratio:.0%} маркеров)"
    else:
        return "Не определено"


def detector(tags_string):
    slova = tags_string.strip().split()

    v_index = -1
    for i, token in enumerate(slova):
        if token == 'V':
            v_index = i
            break

    s_index = -1
    for i, token in enumerate(slova):
        if token in ('N', 'PRO'):
            s_index = i
            break

    if s_index == -1 or v_index == -1:
        return "Unknown"

    o_index = -1
    for i in range(len(slova)):
        if slova[i] in ('N', 'PRO') and i != s_index:
            o_index = i
            break

    if o_index == -1:
        return "Unknown"

    if s_index < v_index < o_index:
        return "SVO"
    elif s_index < o_index < v_index:
        return "SOV"
    elif v_index < s_index < o_index:
        return "VSO"
    else:
        return "Unknown"


def format_guess(word_order: str, alignment: str, morphology: str) -> str:
    database = {
        # ========= SOV =========
        ('SOV', 'Ergative', 'Agglutinative'):
            ('Кавказ, Гималаи, Австралия, Баски',
             'чеченский, тибетский, варлпири, баскский'),
        ('SOV', 'Ergative', 'Fusional'):
            ('возможно, Древний Ближний Восток (шумерский), отдельные австралийские',
             'шумерский'),
        ('SOV', 'Ergative', 'Isolating'):
            None,
        ('SOV', 'Ergative', 'Polysynthetic'):
            ('Арктика и Субарктика, Сибирь',
             'инуктитут, чукотский'),
        ('SOV', 'Ergative', 'Unknown'):
            ('Кавказ, Гималаи, Австралия, Арктика',
             'чеченский, тибетский, варлпири, инуктитут'),

        ('SOV', 'Accusative', 'Agglutinative'):
            ('Алтайский регион, Япония/Корея, Южная Индия',
             'турецкий, монгольский, японский, корейский, тамильский'),
        ('SOV', 'Accusative', 'Fusional'):
            ('Южная Азия, древняя Европа',
             'хинди, санскрит, латынь'),
        ('SOV', 'Accusative', 'Isolating'):
            None,
        ('SOV', 'Accusative', 'Polysynthetic'):
            ('Папуа-Новая Гвинея, возможно Амазония',
             'йимас'),
        ('SOV', 'Accusative', 'Unknown'):
            ('Азия (алтайские, дравидийские, индоарийские), Папуа',
             'турецкий, тамильский, хинди, йимас'),

        ('SOV', 'Unknown', 'Agglutinative'):
            ('алтайские, дравидийские, кавказские',
             'турецкий, тамильский, чеченский'),
        ('SOV', 'Unknown', 'Fusional'):
            ('индоарийские, древние индоевропейские',
             'хинди, латынь'),
        ('SOV', 'Unknown', 'Isolating'):
            ('возможно, тибето-бирманские',
             'бирманский'),
        ('SOV', 'Unknown', 'Polysynthetic'):
            ('эскимосско-алеутские, чукотско-камчатские',
             'инуктитут, чукотский'),
        ('SOV', 'Unknown', 'Unknown'):
            ('Евразия (от Турции до Японии)',
             'турецкий, японский, корейский'),

        # ========= SVO =========
        ('SVO', 'Ergative', 'Agglutinative'):
            ('редко: отдельные папуасские или австронезийские с эргативными чертами',
             'возможны некоторые языки Папуа'),
        ('SVO', 'Ergative', 'Fusional'):
            None,
        ('SVO', 'Ergative', 'Isolating'):
            None,
        ('SVO', 'Ergative', 'Polysynthetic'):
            ('возможно, отдельные языки Северной Америки',
             'некоторые салишские языки'),
        ('SVO', 'Ergative', 'Unknown'):
            ('очень редкое сочетание, возможно расщеплённая эргативность',
             'языки с эргативными чертами'),

        ('SVO', 'Accusative', 'Agglutinative'):
            ('Юго-Восточная Азия, Африка, Европа',
             'индонезийский, суахили, финский'),
        ('SVO', 'Accusative', 'Fusional'):
            ('Европа, Ближний Восток',
             'испанский, русский, арабский'),
        ('SVO', 'Accusative', 'Isolating'):
            ('Восточная и Юго-Восточная Азия, Европа',
             'китайский, тайский, вьетнамский, английский'),
        ('SVO', 'Accusative', 'Polysynthetic'):
            None,
        ('SVO', 'Accusative', 'Unknown'):
            ('Европа, Юго-Восточная Азия, Африка',
             'английский, китайский, суахили'),

        ('SVO', 'Unknown', 'Agglutinative'):
            ('индонезийские, банту, финно-угорские',
             'индонезийский, суахили, финский'),
        ('SVO', 'Unknown', 'Fusional'):
            ('романские, славянские, семитские',
             'испанский, русский, арабский'),
        ('SVO', 'Unknown', 'Isolating'):
            ('Юго-Восточная Азия, английский',
             'китайский, тайский, вьетнамский, английский'),
        ('SVO', 'Unknown', 'Polysynthetic'):
            None,
        ('SVO', 'Unknown', 'Unknown'):
            ('Европа, Юго-Восточная Азия, Африка',
             'английский, китайский'),

        # ========= VSO =========
        ('VSO', 'Ergative', 'Agglutinative'):
            ('Мезоамерика (майянские языки)',
             'киче, юкатекский'),
        ('VSO', 'Ergative', 'Fusional'):
            ('возможно, отдельные майянские с элементами фузии',
             'некоторые майянские'),
        ('VSO', 'Ergative', 'Isolating'):
            None,
        ('VSO', 'Ergative', 'Polysynthetic'):
            ('Северная Америка (сэлишские, вакашские)',
             'нуу-ча-нульт, лушуцид'),
        ('VSO', 'Ergative', 'Unknown'):
            ('Мезоамерика, северо-западное побережье Америки',
             'киче, нуу-ча-нульт'),

        ('VSO', 'Accusative', 'Agglutinative'):
            ('Филиппины',
             'тагальский'),
        ('VSO', 'Accusative', 'Fusional'):
            ('Кельтские языки, берберские, классический арабский',
             'валлийский, ирландский, арабский'),
        ('VSO', 'Accusative', 'Isolating'):
            ('Полинезия',
             'гавайский, маори'),
        ('VSO', 'Accusative', 'Polysynthetic'):
            ('возможно, отдельные сэлишские',
             'некоторые сэлишские'),
        ('VSO', 'Accusative', 'Unknown'):
            ('кельтские, семитские, филиппинские, полинезийские',
             'валлийский, арабский, тагальский, гавайский'),

        ('VSO', 'Unknown', 'Agglutinative'):
            ('филиппинские, майянские, океанийские',
             'тагальский, киче'),
        ('VSO', 'Unknown', 'Fusional'):
            ('кельтские, арабский',
             'валлийский, арабский'),
        ('VSO', 'Unknown', 'Isolating'):
            ('полинезийские',
             'гавайский, маори'),
        ('VSO', 'Unknown', 'Polysynthetic'):
            ('сэлишские, вакашские',
             'нуу-ча-нульт'),
        ('VSO', 'Unknown', 'Unknown'):
            ('кельтские, семитские, австронезийские, майянские',
             'валлийский, арабский, тагальский, киче'),

        # ========= Unknown word order =========
        ('Unknown', 'Ergative', 'Agglutinative'):
            ('Кавказ, Гималаи, Австралия, Баски',
             'чеченский, тибетский, варлпири, баскский'),
        ('Unknown', 'Ergative', 'Fusional'):
            ('Древний Ближний Восток, отдельные австралийские',
             'шумерский'),
        ('Unknown', 'Ergative', 'Isolating'):
            None,
        ('Unknown', 'Ergative', 'Polysynthetic'):
            ('Арктика, Чукотка',
             'инуктитут, чукотский'),
        ('Unknown', 'Ergative', 'Unknown'):
            ('Кавказ, Австралия, Гималаи, Арктика, Мезоамерика',
             'чеченский, варлпири, тибетский, инуктитут, киче'),

        ('Unknown', 'Accusative', 'Agglutinative'):
            ('тюркские, монгольские, дравидийские, финно-угорские, банту',
             'турецкий, монгольский, тамильский, финский, суахили'),
        ('Unknown', 'Accusative', 'Fusional'):
            ('индоевропейские, семитские',
             'хинди, русский, арабский'),
        ('Unknown', 'Accusative', 'Isolating'):
            ('Юго-Восточная Азия, Океания, Западная Африка',
             'китайский, английский, тайский, вьетнамский'),
        ('Unknown', 'Accusative', 'Polysynthetic'):
            ('редко: Папуа',
             'йимас'),
        ('Unknown', 'Accusative', 'Unknown'):
            ('повсеместно',
             'русский, английский, китайский, суахили'),

        ('Unknown', 'Unknown', 'Agglutinative'):
            ('тюркские, финно-угорские, дравидийские, банту, кавказские',
             'турецкий, финский, тамильский, суахили, чеченский'),
        ('Unknown', 'Unknown', 'Fusional'):
            ('индоевропейские, семитские',
             'хинди, русский, арабский'),
        ('Unknown', 'Unknown', 'Isolating'):
            ('Юго-Восточная Азия, Океания, Западная Африка',
             'китайский, вьетнамский, йоруба'),
        ('Unknown', 'Unknown', 'Polysynthetic'):
            ('Сибирь, Северная Америка, Амазония, Папуа',
             'чукотский, инуктитут, мапуче, йимас'),
        ('Unknown', 'Unknown', 'Unknown'):
            ('недостаточно данных',
             'неизвестны'),
    }

    key = (word_order, alignment, morphology)
    entry = database.get(key)

    if entry is None:
        return None

    areas, examples = entry
    return (f"Ареалы распространения: {areas}.\n"
            f"Примеры языков: {examples}.\n"
            f"Порядок слов: {param_label(word_order)}.\n"
            f"Строй языка: {param_label(alignment)}.\n"
            f"Тип морфологической структуры: {param_label(morphology)}.")


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


def glossing_machine(glossed, tags):
    align_result = alignment(glossed)
    main_type, has_alt = morph(glossed)
    word_order = detector(tags)

    align_map = {
        'Эргативная': 'Ergative',
        'Аккузативная': 'Accusative',
        'Расщеплённая эргативность': 'Unknown',
        'Не определено': 'Unknown'
    }
    align_key = align_result.split()[0]
    align = align_map.get(align_key, 'Unknown')

    # Получаем результат для основного типа
    res_main = format_guess(word_order, align, main_type)

    if not has_alt:
        if res_main is None:
            return "простите по данному отрывку невозможно определить ареал распространения языка"
        return res_main

    # Есть альтернатива: пытаемся получить результат для альтернативного типа
    alt_type = 'Fusional' if main_type == 'Agglutinative' else 'Agglutinative'
    res_alt = format_guess(word_order, align, alt_type)

    if res_alt is None:
        if res_main is None:
            return "простите по данному отрывку невозможно определить ареал распространения языка"
        return res_main + f"\n\nПримечание: возможно также {param_label(alt_type)} (но данные о таком сочетании отсутствуют)."

    # Разбираем строки
    lines_main = res_main.split('\n')
    lines_alt = res_alt.split('\n')

    # Объединяем ареалы и примеры через " / "
    areas_main = lines_main[0].split(':', 1)[1].strip()
    areas_alt = lines_alt[0].split(':', 1)[1].strip()
    combined_areas = f"Ареалы распространения: {areas_main} (возможно: {areas_alt})"

    examples_main = lines_main[1].split(':', 1)[1].strip()
    examples_alt = lines_alt[1].split(':', 1)[1].strip()
    combined_examples = f"Примеры языков: {examples_main} (возможно: {examples_alt})"

    # Порядок слов и строй языка берём из основного
    word_order_line = lines_main[2]
    alignment_line = lines_main[3]

    # Тип морфологической структуры объединённый
    morphology_line = f"Тип морфологической структуры: {param_label(main_type)}, но возможен {param_label(alt_type)}."

    result = f"{combined_areas}\n{combined_examples}\n{word_order_line}\n{alignment_line}\n{morphology_line}"
    return result


if __name__ == "__main__":
    text = input("Введите Ваш текст (глоссы строго через дефис, ПРИМЕР: я-ERG-1SG собака-ABS видеть-PST-PFV): ")
    vso = input("Введите теги частей речи через пробел (N – noun, V – verb, PRO – pronoun и т.д.): ")
    result = glossing_machine(text, vso)
    print(result)
